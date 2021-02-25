#!/usr/bin/env bash

PREV_DIR=$(pwd)
mkdir -p ~/.pb
wget -O ~/.pb/build.zip https://raw.githubusercontent.com/thepeshka/pb/main/builds/linux/latest/build.zip
cd ~/.pb || exit
unzip build.zip > /dev/null
rm ./build.zip
cd "$PREV_DIR" || exit
echo "PATH=$PATH:~/.pb #ADDED BY PB INSTALLER" >> ~/.bashrc
echo "#!/bin/bash

awk '!/#ADDED BY PB INSTALLER$/' ~/.bashrc > ~/.bashrc
rm -r ~/.pb
exec \"\$SHELL\"
" > ~/.pb/pb-uninstall
chmod +x ~/.pb/pb-uninstall
exec "$SHELL"
