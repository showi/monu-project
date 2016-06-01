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
        log.info('Searching ingredient: %s', search)
        with mdb.util.open() as handle:
            for doc in mdb.util.find(handle.ingredient, search):
                log.info('doc %s', doc)
                mdb.util.astrid(doc)
                response.append(doc)
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")
