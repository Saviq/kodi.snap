#!/usr/bin/env python3

from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent
from urllib import parse

import requests
import hiyapyco

ADDONS_REPO = "https://github.com/xbmc/repo-binary-addons.git"
DEPENDENCY_ROOT = "https://raw.githubusercontent.com/{owner}/{repo}/{branch}/depends/common/{dep}/"
ADDONS_BRANCH = "Piers"
SOURCE = "snap/local/snapcraft.yaml.in"
TARGET = "snap/snapcraft.yaml"

DENY_LIST = {"audiodecoder.dumb", "audiodecoder.modplug"}

CMAKE_PARAMETERS = {
    "plugin": "cmake",
    "cmake-generator": "Ninja",
    "cmake-parameters": [
        "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
        "-DCMAKE_INSTALL_PREFIX=/usr",
        "-DCMAKE_MODULE_PATH=${CRAFT_STAGE}/usr/share/kodi/cmake",
        "-DKODI_INCLUDE_DIR=${CRAFT_STAGE}/usr/include/kodi/",
        "-DCORE_SYSTEM_NAME=linux",
    ]
}

PRIME_DEBUGINFO = dedent("""
    set -euo pipefail
    craftctl default

    DEBUGINFO="${CRAFT_COMPONENT_DEBUG_PRIME}/debug/.build-id"

    cd ${CRAFT_PART_INSTALL}

    IFS=$'\\n'; for file in $( find . -type f ); do
      FILE_TYPE="$( file --brief -e apptype -e ascii -e encoding -e cdf -e compress -e tar -- "${file}" )"
      [[ "${FILE_TYPE}" == *"not stripped" ]] || continue
      if ! [[ "${FILE_TYPE}" =~ BuildID\\[[^\\]]+\\]=([0-9a-f]{2})([0-9a-f]+) ]]; then
        ( echo "WARNING: BuildId not found for ${file}")
        continue
      fi
      mkdir --parents "${DEBUGINFO}/${BASH_REMATCH[1]}"
      debug_file="${DEBUGINFO}/${BASH_REMATCH[1]}/${BASH_REMATCH[2]}.debug"
      objcopy --only-keep-debug --compress-debug-sections "${CRAFT_PRIME}/${file}" "${debug_file}"
      chmod 644 "${debug_file}"
      strip --remove-section=.comment --remove-section=.note --strip-unneeded "${file}"
    done
""")

source_craft = hiyapyco.load(SOURCE)
parts = {
    "kodi": {
        "override-prime": PRIME_DEBUGINFO,
    }
}

def retrieve_dep(filename, vars, method=requests.get):
    if (r := method((DEPENDENCY_ROOT + filename).format(**vars))) and r.status_code == 200:
        return r.content.strip().decode("utf-8")
    elif r.status_code == 404:
        return None
    else:
        r.raise_for_status()

with TemporaryDirectory() as tmp:
    subprocess.run(("git", "clone", ADDONS_REPO, "--branch", ADDONS_BRANCH, "--depth=1", tmp), check=True)

    for platforms in sorted(Path(tmp).glob("*/platforms.txt")):
        with open(platforms) as f, open(platforms.parent / (platforms.parent.name + ".txt")) as f2:
            platforms = set(next(f).strip().split())
            addon, repourl, branch = next(f2).strip().split()

        if addon in DENY_LIST:
            continue

        if (platforms.intersection({"all", "linux"})
            or all(platform.startswith("!") for platform in platforms)):

            after = source_craft["parts"].get(addon, {}).get("after", [])
            for dep in after:
                owner, repo = Path(parse.urlparse(repourl).path).parts[1:3]
                _, source = retrieve_dep("{dep}.txt", locals()).split()
                parts[dep] = {
                    "source": source,
                    **CMAKE_PARAMETERS,
                    "override-prime": PRIME_DEBUGINFO,
                }

                if (retrieve_dep("CMakeLists.txt", locals(), requests.head) is not None):
                    parts[dep]["build-packages"] = ["curl"]
                    parts[dep]["override-pull"] = dedent(
                        f"""
                        craftctl default
                        curl -o ${{CRAFT_PART_SRC}}/CMakeLists.txt {(DEPENDENCY_ROOT + "CMakeLists.txt").format(**locals())}
                        """
                    )

                if (checksum := retrieve_dep("{dep}.sha256", locals())):
                    parts[dep]["source-checksum"] = f"sha256/{checksum}"

                if (flags := retrieve_dep("flags.txt", locals())):
                    parts[dep]["cmake-parameters"] = parts[dep]["cmake-parameters"] + flags.split()

            parts[addon] = {
                **CMAKE_PARAMETERS,
                "override-prime": PRIME_DEBUGINFO,
                "after": ["kodi"] + after,
                "source": f"{repourl}.git",
                "source-branch": branch,
                "source-depth": 1,
            }

parts["gpu-2404"] = {
    "after": ["kodi", *(addon for addon in parts)]
}

craft = hiyapyco.load(hiyapyco.dump({"parts": parts}), SOURCE, method=hiyapyco.METHOD_MERGE)

with open(TARGET, "w", encoding="utf-8") as f:
    f.write(hiyapyco.dump(craft))
