# Kodi Snap

This is the [Kodi](https://kodi.tv) media center software, packaged as a snap.

Kodi is an award-winning free and open source software media player and
entertainment hub for digital media. Available as a native application for
Android, Linux, BSD, macOS, iOS, tvOS and Windows operating systems, Kodi runs
on most common processor architectures.

Created in 2003 by a group of like minded programmers, Kodi is a non-profit
project run by the XBMC Foundation and developed by volunteers located around
the world. More than 500 software developers have contributed to Kodi to date,
and 100-plus translators have worked to expand its reach, making it available
in more than 70 languages.

While Kodi functions very well as a standard media player application for your
computer, it has been designed to be the perfect companion for your HTPC. With
its beautiful interface and powerful skinning engine, Kodi feels very natural
to use from the couch with a remote control and is the ideal solution for your
home theater.

______________________________________________________________________

## Interfaces:

These give Kodi access to different system resources. You can decide, which
accesses you want to allow.
See more on [Snap interfaces documentation](https://snapcraft.io/docs/interfaces).

- `gpu-2404`
  Provides the userspace GPU drivers, enabling rendering and video decoding
  acceleration. See [The gpu-2404 snap interface](https://mir-server.io/docs/the-gpu-2404-snap-interface)
  for more information.
  This will normally be connected to the [`mesa-2404`](https://snapcraft.io/mesa-2404/)
  snap, serving all open source drivers and Nvidia userspace from the host
  system, where possible.

- `ffmpeg-2404`
  This gives Kodi access to the latest FFmpeg for media decoding capabilities.
  See upstream [ffmpeg-2404](https://snapcraft.io/ffmpeg-2404) for more.

- `alsa`
  `audio-playback`
  `jack1`
  Audio playback subsystems.

- `opengl`
  `wayland`
  `x11`
  Graphics hardware and the respective windowing systems.

- `joystick`
  `raw-input`
  `raw-usb`
  Input devices, at least `raw-input` is required for operation without a
  display server (using the gbm backend).

- `mount-observe`
  `optical-drive`
  `removable-media`
  `udisks2`
  External storage.

- `home`
  The running user's home folder (except for hidden folders).

- `avahi-control`
  Broadcast Kodi services on the local network for e.g. remote control.

- `network`
  `network-bind`
  Access and expose services on the network.

- `shutdown`
  Power the system down.

- `hardware-observe`
  `upower-observe`
  Enumerate hardware and power properties of the system.

## Desktop sessions:

To use Kodi as your login session,

```
snap connect kodi:desktop-sessions
snap connect kodi:login-session-control
snap connect kodi:raw-input
```

This allows you to select Kodi when logging in to your machine. This reduces
resource usage, as Kodi is the only application running. You need the
`raw-input` interface connected as well and permissions to access
`/dev/input` devices (usually through membership of the `input` group) to
control it with keyboard and mice.

## Configuration options:

- `daemon`
  One of `{false,gbm,wayland}`, making Kodi start up on boot. The `wayland`
  mode is geared at usage with a Wayland compositor running as a daemon
  as well - for example [Ubuntu Frame](https://snapcraft.io/ubuntu-frame).

See [https://snapcraft.io/kodi](https://snapcraft.io/kodi) for more information.
