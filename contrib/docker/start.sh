#!/usr/bin/sh
export PYTHONPATH="."
echo "127.0.0.1 db" >> /etc/hosts
mkdir -p /tmp/monu
/etc/init.d/mongodb start
python monu/script/install_data.py
python httpd
