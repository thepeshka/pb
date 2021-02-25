#!/bin/bash

set -e

BUILD_LOG=$(pwd)/build.log
VERSION=$(cat VERSION)
echo "Building pb ${VERSION}" > "${BUILD_LOG}"

echo -n "Building ... "
echo "cxfreeze -c pb.py --target-dir dist" >> "${BUILD_LOG}"
cxfreeze -c pb.py --target-dir dist >> "${BUILD_LOG}"
echo "DONE"

echo -n "Zipping ... "
cd dist || exit
echo "zip -r build.zip ./*" >> "${BUILD_LOG}"
zip -r build.zip ./* >> "${BUILD_LOG}"
echo "DONE"

cd ..
echo -n "Setting versions ... "
mkdir -p "builds/linux/${VERSION}"
mkdir -p "builds/linux/latest"
cp ./dist/build.zip "builds/linux/${VERSION}"
cp ./dist/build.zip "builds/linux/latest"
echo "DONE"

echo -n "Cleaning up ... "
rm -r ./dist
echo "DONE"
