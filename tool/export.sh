#!/bin/bash

if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

rev1="$1"

if [ "x${rev1}" != "xexp" ] && [ "x${rev1}" != "xmaster" ]; then
    echo "Usage: $(basename $0) {master|exp} "
    exit 1
fi

cd /opt/git/aoaola.git
git archive ${rev1} -o /tmp/aoaola.tgz
ret=$?
if [ "x${ret}" != "x0" ]; then
    echo "An error occurs when archiving."
    exit 1
fi

if [ "${rev1}" == "master" ]; then
    cd /opt/aoaola
elif [ "${rev1}" == "exp" ]; then
    cd /opt/aoaola_exp
fi

tar xf /tmp/aoaola.tgz

if [ "${rev1}" == "master" ]; then
    sed -i "s/^#web.config.debug = False/web.config.debug = False/"  /opt/aoaola/web/cgi/app.py
    sed -i "s/^#app.add_processor(cache.cachePage)/app.add_processor(cache.cachePage)/"  /opt/aoaola/web/cgi/app.py
    sed -i "s/'HOST_NAME' : 'http:\/\/me.aoaola.com'/'HOST_NAME' : 'http:\/\/aoaola.com'/"  /opt/aoaola/web/cgi/site_helper.py
    chown www-data:www-data -R /opt/aoaola
    /opt/aoaola/tool/spawn-fcgi.sh restart
    cd /opt/aoaola/web/plugins/zarkfx
    git pull origin master
elif [ "${rev1}" == "exp" ]; then
    sed -i "s/'APP_PORT' : 20004/'APP_PORT' : 20006/" /opt/aoaola_exp/web/cgi/site_helper.py
    sed -i "s/'APP_ROOT_PATH' : '\/opt\/aoaola\/'/'APP_ROOT_PATH' : '\/opt\/aoaola_exp\/'/"  /opt/aoaola_exp/web/cgi/site_helper.py
    sed -i "s/'SESSION_PATH' : '\/opt\/aoaola\/web\/sessions'/'SESSION_PATH' : '\/opt\/aoaola_exp\/web\/sessions'/"  /opt/aoaola_exp/web/cgi/site_helper.py
    sed -i "s/'ERROR_LOG_PATH' : ''/'ERROR_LOG_PATH' : '\/var\/log\/aoaola\/error_exp.log'/"  /opt/aoaola_exp/web/cgi/site_helper.py
    sed -i "s/^#web.config.debug = False/web.config.debug = False/"  /opt/aoaola_exp/web/cgi/app.py
    sed -i "s/^#app.add_processor(cache.cachePage)/app.add_processor(cache.cachePage)/"  /opt/aoaola_exp/web/cgi/app.py
    sed -i "s/'HOST_NAME' : 'http:\/\/me.aoaola.com'/'HOST_NAME' : 'http:\/\/exp.aoaola.com'/"  /opt/aoaola_exp/web/cgi/site_helper.py
    chown www-data:www-data -R /opt/aoaola_exp
    /opt/aoaola_exp/tool/spawn-fcgi-exp.sh restart
    cd /opt/aoaola_exp/web/plugins/zarkfx
    git pull origin master
fi

