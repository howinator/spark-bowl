#!/usr/bin/env bash

BUNDLE_NAME=$1
DEPLOY_DIR=$2

cd "$DEPLOY_DIR/" || (1>&2 echo "could not cd into DEPLOY_DIR" && exit 1)

rm -rf build
mkdir build

BUILD_PARENT_DIR=$(pwd)

cd "$DEPLOY_DIR/.venv-spark/lib/python2.7/site-packages/" || (1>&2 echo "could not cd into venv/lib" && exit 1)
zip -qr "$BUILD_PARENT_DIR/build/$BUNDLE_NAME" ./*

cd "$DEPLOY_DIR/.venv-spark/lib64/python2.7/site-packages" || (1>&2 echo "could not cd into venv/lib64" && exit 1)
zip -qr "$BUILD_PARENT_DIR/build/$BUNDLE_NAME" ./*

cd "$BUILD_PARENT_DIR/src" || (1>&2 echo "could not cd into src" && exit 1)

zip -qur "$BUILD_PARENT_DIR/build/$BUNDLE_NAME" ./* -x "tests.py" -x "*.pyc"