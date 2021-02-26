#!/usr/bin/env bash

PREV_DIR=$(pwd)
mkdir -p ~/.pb
curl --output "$HOME/.pb/build.zip" https://raw.githubusercontent.com/thepeshka/pb/main/builds/linux/latest/build.zip
cd ~/.pb || exit
unzip build.zip > /dev/null
rm ./build.zip
cd "$PREV_DIR" || exit
echo "Get your keys at https://pastebin.com/doc_api. User key is optional."
echo "Add these lines to ~/.bashrc:
  export PATH=\"\$PATH:~/.pb\"
  export PB_API_DEV_KEY=\"<dev key>\"
  export PB_API_USER_KEY=\"<dev key>\""
