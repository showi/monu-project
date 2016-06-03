#!/usr/bin/env sh

if [ ! -d env ]; then
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
fi
