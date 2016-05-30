#!/usr/bin/sh

export PYTHONPATH="."
mkdir /tmp/monu
python monu/mdb/install_data.py
#python monu/db.py
python httpd
