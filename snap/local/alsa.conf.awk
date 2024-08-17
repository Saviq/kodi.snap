BEGIN {
    part="";
}

/"~\/.asoundrc"/ {
    part="";
    print "\t\t\t{"
    print "\t\t\t\t@func concat"
    print "\t\t\t\tstrings ["
    print "\t\t\t\t\t{"
    print "\t\t\t\t\t\t@func getenv"
    print "\t\t\t\t\t\tvars ["
    print "\t\t\t\t\t\t\tSNAP"
    print "\t\t\t\t\t\t]"
    print "\t\t\t\t\t\tdefault \"/snap/kodi/current\""
    print "\t\t\t\t\t}"
    print "\t\t\t\t\t\"/usr/share/alsa/alsa.conf.d\""
    print "\t\t\t\t]"
    print "\t\t\t}"
}

{
    if (part == "files") next;
    print;
}

/^@hooks/ {
    part="hooks";
}

/files \[/ {
    if (part == "hooks") part="files";
}


