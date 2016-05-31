# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime
import uuid
import flask
from flask_restful import Resource
from monu.conf import conf
from monu.logger import getLogger
from monu.srv.authentication import requires_auth
from monu.srv.argument import parser_factory
from monu.mdb import common as db
from monu import schema

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




class Ref(Resource):
    @requires_auth
    def get(self, collection=None, key=None, value=None):
        response = {'doc': [], 'total': 0}
        for doc in db.find(db.open()[collection], key=key, value=value):
            response['doc'].append(doc)
            response['total'] += 1
        return response
