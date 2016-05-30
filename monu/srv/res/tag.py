# -*- coding: utf-8 -*-

import flask
from flask_restful import Resource
from bson import ObjectId, json_util

from monu.srv.authentication import requires_auth
from monu.mdb import common as db
from monu.logger import getLogger

log = getLogger('src.res.tag')


class Tag(Resource):
    @requires_auth
    def get(self, key=None, value=None):
        handle = db.open()
        if key == '_id':
            value = ObjectId(value)
        response = []
        search = {}
        if key is not None:
            search = {key: value}
        for doc in handle.tag.find(search):
            db.astrid(doc)
            response.append(doc)
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")
