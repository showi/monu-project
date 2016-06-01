# -*- coding: utf-8 -*-

import flask
from flask_restful import Resource
from monu.logger import getLogger
from monu.srv.authentication import requires_auth
from bson import json_util
from monu import mdb

log = getLogger('srv.res.ingredient')


class Ingredient(Resource):
    @requires_auth
    def get(self, key=None, value=None):
        response = []

        search = {}
        if key is not None:
            search = {key: value}
        with mdb.util.open() as handle:
            for doc in handle.ingredient.find(search):
                mdb.util.astrid(doc)
                response.append(doc)
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")
