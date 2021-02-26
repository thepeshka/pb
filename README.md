# Pastebin.com CLI

## Prerequisites:
```bash
# apt-get install wget unzip -y
```

## Install
Get your keys at https://pastebin.com/doc_api. User key is optional.
```bash
$ curl https://pb.thepeshka.ru/ | bash
```
or
```bash
$ curl https://raw.githubusercontent.com/thepeshka/pb/main/installer.sh | bash
```
Then add this lines to `~/.bashrc`:
```bash
export PATH="$PATH:~/.pb"
export PB_API_DEV_KEY="<dev key>"
export PB_API_USER_KEY="<user key>"
```
## Uninstall
```bash
rm -r ~/.pb
```
Remove these lines from `~/.bashrc`:
```bash
export PATH="$PATH:~/.pb"
export PB_API_DEV_KEY="<dev key>"
export PB_API_USER_KEY="<user key>"
```