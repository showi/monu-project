# -*- coding: utf-8 -*-
import os
import re
import dateutil.parser
from datetime import datetime
import uuid
import json
import flask
from flask_restful import Resource
from monu.conf import conf
from monu.logger import getLogger
from monu.srv.authentication import requires_auth
from bson import json_util
from monu.mdb import common as db

log = getLogger('srv.res.ingredient')


class Ingredient(Resource):
    @requires_auth
    def get(self, key=None, value=None):
        response = []
        handle = db.open()

        search = {}
        if key is not None:
            search = {key: value}
        for doc in handle.ingredient.find(search):
            db.astrid(doc)
            response.append(doc)
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")
