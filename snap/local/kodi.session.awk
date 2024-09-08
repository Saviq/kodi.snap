/^Name=/ { print "Name=Kodi (Snap)"; next }
/^Exec=/ { print "Exec=snap run kodi --standalone --windowing=gbm"; next }
/^TryExec=/ { next }
{ print }
