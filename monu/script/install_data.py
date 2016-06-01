#!/usr/bin/env python
# -*- coding: utf-8 -*-

from monu.mdb import common as mdb

with mdb.open() as db:
    mdb.remove_all(db.tag)
    mdb.remove_all(db.ingredient)
    mdb.remove_all(db.recipe)
    mdb.preload_collection(db)
