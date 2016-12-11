#!/usr/bin/env bash
set -ex

usage() {
    echo 'usage: sshi-pi.sh USERNAME' >&2
    exit 1
}

if [ $# != 1 ]; then
    usage
fi

USERNAME=$1

ssh -p 50069 "${USERNAME}"@"$(arp -a | grep 'b8:27:eb:a2:73:e2' | grep -o '[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}')"
