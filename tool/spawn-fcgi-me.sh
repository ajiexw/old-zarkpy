#!/bin/bash

if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

PWD="/opt/songshu/web/cgi"
PIDFILE="/var/run/songshu-local-spawn-fcgi.pid"

case $1 in
    "start")
        export PYTHON_EGG_CACHE="/tmp/.python-eggs"
        cp "${PIDFILE}" "${PIDFILE}.bak" 2>/dev/null
        spawn-fcgi -f "${PWD}/app.py" -d "${PWD}" -a 127.0.0.1 -p 10000 \
            -F 1 -P "${PIDFILE}" -u ajie -g ajie
        ret=$?
        if [ "x${ret}" == "x0" ]; then
            echo "" >> "${PIDFILE}"
            rm "${PIDFILE}.bak" 2>/dev/null
        else
            mv "${PIDFILE}.bak" "${PIDFILE}" 2>/dev/null
        fi
        exit ${ret}
        ;;
    "stop")
        if [ -f "${PIDFILE}" ]; then
            while read pid; do
                if [[ -d "/proc/${pid}" && \
                    $(stat -c "%U %G" "/proc/${pid}") == \
                    "ajie ajie" ]]; then
                    grep "app.py" "/proc/${pid}/cmdline" 1>/dev/null 2>&1
                    if [ "x$?" == "x0" ]; then
                        kill -KILL ${pid}
                    fi
                fi
            done < "${PIDFILE}"
            rm "${PIDFILE}" 2>/dev/null
        fi
        ;;
    "restart")
        $0 stop
        $0 start
        ;;
    *)
        echo "usage: $(basename $0) {start|stop}"
        exit 1
        ;;
esac
