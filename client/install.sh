#!/usr/bin/env bash


echo "Installing spc command line tool"

sudo cp -rf Linux_Client/{spc,myscript.py,aes.py,arc4.py,sync.py,blowfish.py,file_status.py,modify_scheme.py} /usr/bin/

cp Linux_Client/sync.cron Linux_Client/notify.sh ~/
chmod +x ~/notify.sh

crontab ~/sync.cron

pip3 install -r requirements.txt



