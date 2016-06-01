#!/usr/bin/sh
export PYTHONPATH="."
mkdir -p /tmp/monu
python monu/script/install_data.py
python httpd
