# -*- coding: utf-8 -*-

from flask_restful import Resource

from monu.logger import getLogger
from monu.mdb import common as db
from monu.schema import SCHEMA
log = getLogger('srv.res.schema')

class Schema(Resource):
    def get(self, name=None):
        if name is None:
            return SCHEMA
        return db.get_schema(db.open(), name)

