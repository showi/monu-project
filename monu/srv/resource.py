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
from monu.srv.common import res2dct
from monu.srv.argument import parser_factory
from monu.util import hashit, pretty_dict
from monu.mdb import common as db
from monu import schema
from bson.dbref import DBRef
from bson import ObjectId, json_util
from monu.srv.res.ingredient import Ingredient
from monu.srv.res.recipe import Recipe
from monu.srv.res.tag import Tag

log = getLogger('res')

__RE_FLAGS__ = re.UNICODE & re.IGNORECASE
__AES_KEYLENGTH__ = 32
PUBUUID = str(uuid.uuid4())

parser = parser_factory()
utcnow = datetime.utcnow


class File(Resource):
    def get(self, name=None):
        parser = parser_factory(namespace='file',
                                locations=['values', 'json', 'headers'])
        args = parser.parse_args()
        path = os.path.join(conf.get('backend.storage', 'path'), name)
        log.info('Requesting file with hash: %s', path)
        if not os.path.exists(path):
            return "File not found", 404
        return flask.send_file(path,
                               args.mime)  # , as_attachment, attachment_filename, add_etags, cache_timeout, conditional)


import copy


def get_schema(handle, name):
    s = copy.deepcopy(schema.SCHEMA[name])
    # if name == 'ingredient':
    # for doc in db.find(handle.tag):
    # s['tag']['items']['properties']['type']['enum'].append({
    #    '_id': doc['_id'],
    #    'name': doc['name']
    # })
    return s


class Schema(Resource):
    def get(self, name=None):
        if name is None:
            return SCHEMA
        return get_schema(db.open(), name)


class Ref(Resource):
    @requires_auth
    def get(self, collection=None, key=None, value=None):
        response = {'doc': [], 'total': 0}
        for doc in db.find(db.open()[collection], key=key, value=value):
            response['doc'].append(doc)
            response['total'] += 1
        return response


def digestify(doc, keyring=['ingredient', 'child', 'step']):
    if 'child' in doc:
        for child in doc['child']:
            digestify(child, keyring)
    for key in keyring:
        if key in doc:
            del doc[key]
