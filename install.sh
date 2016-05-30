#~!/usr/bin/env bash
echo --- --- --- --- ---
echo Installing monu 
echo  - os: Linux
echo  - brand: Arch
echo --- --- --- --- ---
cwd=`pwd`
RBVERSION="2.2.0"

deactivate 2> /dev/null
if [ ! -d env/ ]; then
    echo ">>> Creating python virtualenv"
    virtualenv --python=python2.7 --no-site-packages env
fi
source env/bin/activate
if [ ! -d monu.egg-info ]; then
    echo ">>> Installing monu python egg"
    python setup.py develop
fi
cd monu-ui
echo ">>> Installing npm saved package"
npm install
echo ">>> Installing bower package"
bower install
echo ">>> Building ui (js,html...)"
grunt build
