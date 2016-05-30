#!/usr/bin/sh

export PYTHONPATH="."
mkdir -p /tmp/monu
/etc/init.d/mongodb start
python monu/mdb/install_data.py
python httpd
