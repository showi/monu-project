# -*- coding: utf-8 -*-

import flask
from flask_restful import Resource
from monu.logger import getLogger
from monu.srv.authentication import requires_auth
from bson import json_util, ObjectId
from monu import mdb

log = getLogger('srv.res.ingredient')


class Ingredient(Resource):
    @requires_auth
    def get(self, key=None, value=None):
        response = []
        search = {}
        if key is not None:
            if key == '_id':
                value = ObjectId(value)
            search = {key: value}
        with mdb.util.open() as handle:
            for doc in mdb.util.find(handle.ingredient, search):
                doc = mdb.util.astrid(doc)
                if 'tag' in doc:
                    [mdb.util.astrid(tag) for tag in doc['tag']]
                response.append(doc)
            js = json_util.dumps(response)
        return flask.Response(response=js,
                              status=200,
                              mimetype="application/json")
