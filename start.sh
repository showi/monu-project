#!/usr/bin/sh
export PYTHONPATH="."
mkdir -p /tmp/monu
#/etc/init.d/mongodb start
#echo "127.0.0.1 db" >> /etc/hosts
python monu/script/install_data.py
python monu/mdb/redux.py
#python httpd
