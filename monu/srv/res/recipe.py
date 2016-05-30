# -*- coding: utf-8 -*-
import flask
from flask_restful import Resource
from bson import ObjectId, json_util

from monu.logger import getLogger
from monu.srv.authentication import requires_auth
from monu.mdb import common as db
from monu.srv.common import digestify

log = getLogger('srv.res.recipe')


class Recipe(Resource):
    @requires_auth
    def get(self, key=None, value=None):
        if key == '_id':
            value = ObjectId(value)
        response = []
        handle = db.open()
        search = {}
        if key is not None:
            search = {key: value}
        digest = False
        if key is None:
            digest = True
        for doc in handle.recipe.find(search):
            if 'tag' in doc and doc['tag'] is not None:
                nt = []
                for tag in doc['tag']:
                    if isinstance(tag, basestring):
                        db.astrid(tag)
                        nt.append(tag)
                    else:
                        log.info('Tag %s', tag)
                        newtag = db.deref(handle.tag, tag['_id'])
                        log.info('new tag: %s', newtag)
                        db.astrid(newtag)
                        nt.append(newtag)
                doc['tag'] = nt
            if not digest and 'ingredient' in doc and doc['ingredient'] is not None:
                ni = []
                for ingredient in doc['ingredient']:
                    newing = db.deref(handle.ingredient, ingredient['_id'])
                    if newing is not None:
                        for key in ingredient:
                            if key == 'name':
                                continue
                            newing[key] = ingredient[key]
                        db.astrid(newing)
                        ni.append(newing)
                    else:
                        db.astrid(ingredient)
                        ni.append(ingredient)
                doc['ingredient'] = ni
            if digest:
                digestify(doc)
            db.astrid(doc)
            response.append(doc)
        return flask.Response(response=json_util.dumps(response),
                              status=200,
                              mimetype="application/json")
