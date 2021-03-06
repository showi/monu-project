# -*- coding: utf-8 -*-

import flask
from flask_restful import Resource
from bson import ObjectId, json_util

from monu.logger import getLogger
from monu.srv.authentication import requires_auth
from monu import mdb
from monu.srv.common import digestify

log = getLogger('srv.res.recipe')

import urllib2


def unsplit(l):
    res = []
    for v in l.split(','):
        res.append(urllib2.unquote(v))
    return res


class HasTag(Resource):
    @requires_auth
    def get(self, collection=None, key=None, tag_list=None):
        response = []
        with mdb.util.open() as handle:
            for doc in mdb.redux.has_tag(handle[collection], unsplit(tag_list), key=key).find():
                doc.update(mdb.util.find_one(handle[collection], {'_id': doc['_id']}))
                response.append(digestify(mdb.common.astrid(doc)))
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")


class HasIngredient(Resource):
    @requires_auth
    def get(self, collection=None, key=None, ingredient_list=None):
        response = []
        ingredient_list = unsplit(ingredient_list)
        with mdb.util.open() as handle:
            for doc in mdb.redux.has_ingredient(handle[collection], ingredient_list, key=key).find():
                doc.update(mdb.util.find_one(handle[collection], {'_id': doc['_id']}))
                i = mdb.common.astrid(doc)
                response.append(digestify(i))
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")
