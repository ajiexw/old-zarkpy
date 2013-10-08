#!/bin/bash
if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

indexer --all --rotate
