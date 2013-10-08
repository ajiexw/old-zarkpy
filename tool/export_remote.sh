#!/bin/bash

if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

rev="$1"

if [ "x${rev}" == "x" ]; then
    echo "Usage: $(basename $0) {rev}"
    exit 1
fi

cd ~/aoaola
git archive --remote=origin ${rev} -o /tmp/aoaola.tgz
ret=$?

if [ "x${ret}" != "x0" ]; then
    echo "An error occurs when archiving."
    exit 1
fi

cd /opt/aoaola
tar xf /tmp/aoaola.tgz

chown www-data:www-data -R /opt/aoaola
/opt/aoaola/tool/spawn-fcgi.sh restart
