# -*- coding: utf-8 -*-

import flask
from flask_restful import Resource
from bson import ObjectId, json_util

from monu.logger import getLogger
from monu.srv.authentication import requires_auth
from monu import mdb
from monu.srv.common import digestify

log = getLogger('srv.res.recipe')


class HasTag(Resource):
    @requires_auth
    def get(self, collection=None, tag_list=None):
        # tag_list = tag_list.split(',')
        response = []
        with mdb.util.open() as handle:
            for doc in mdb.redux.has_tag(handle[collection], tag_list.split(',')).find():
                response.append(digestify(mdb.util.find_one(handle[collection], doc['_id'])))
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")


class HasIngredient(Resource):
    @requires_auth
    def get(self, collection=None, ingredient_list=None):
        # tag_list = tag_list.split(',')
        response = []
        with mdb.util.open() as handle:
            for doc in mdb.redux.has_ingredient(handle[collection], ingredient_list.split(',')).find():
                response.append(digestify(mdb.util.find_one(handle[collection], doc['_id'])))
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")
