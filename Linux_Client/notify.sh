#! /bin/bash
export DISPLAY=:0.0
spc --status | sed -n '/^Files wi/,/^--/p' > ~/difftemp
scheme=$(DISPLAY=:0.0 /usr/bin/zenity --entry  --text="You may want to sync your files as a matter of regularity.\n Choose\n 1 for mirroring files on server\n 2 for merging and overwriting on server\n 3 for overwriting on client.\n Cancel if you don't want to sync")
if [ $scheme = 1 ];then
	/usr/bin/spc --sync < 1
fi
if [ $scheme = 2 ];then
	/usr/bin/spc --sync < 2
fi
if [ $scheme = 3 ];then
	/usr/bin/spc --sync < 3
fi
