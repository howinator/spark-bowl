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
ADDRESS=$(arp -a | grep 'b8:27:eb:a2:73:e2' | grep -o '[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}.[0-9]\{1,3\}')

if [ -z "$ADDRESS" ]; then
    ADDRESS=192.168.1.23
fi

ssh -p 50069 "$USERNAME"@"$ADDRESS"
