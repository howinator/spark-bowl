#!/usr/bin/env bash

BUNDLE_NAME=$1

rm -rf build
mkdir build

BUILD_PARENT_DIR=$(pwd)

cd ../.venv-spark/lib/python2.7/site-packages/ || (1>&2 echo "could not cd 1" && exit 1)

zip -qr "$BUILD_PARENT_DIR/build/$BUNDLE_NAME" ./*

cd "$BUILD_PARENT_DIR/src" || (1>&2 echo "could not cd 2" && exit 1)

zip -qur "$BUILD_PARENT_DIR/build/$BUNDLE_NAME" ./* -x "tests.py"