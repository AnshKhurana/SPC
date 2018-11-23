#!/usr/bin/env bash



read -p "Enter the installation directory: " INSTALL_DIR

mkdir -p ${INSTALL_DIR}

sudo cp -rf Linux_Client/{spc, myscript.py, aes.py, arc4.py, sync.py, blowfish.py, file_status.py, modify_scheme.py} /usr/bin/

pip3 install -r requirements.txt



