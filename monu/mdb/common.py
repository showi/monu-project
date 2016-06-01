# -*- coding: utf-8 -*-

import os
import json
import monu
from monu.util import file_as_string
from monu.logger import getLogger
from pymongo import MongoClient
from monu.conf import conf
from monu.mdb.replace import replace

log = getLogger('monu.mdb.common')

schema_path = os.path.join(monu.base_path, 'monu', 'data', 'schema')
collection_path = os.path.join(schema_path, 'collection')

VALID_COLLECTION = [u'ingredient', u'recipe', u'tag']


class Error(object):
    class InvalidCollection(Exception):
        pass


def astrid(data):
    if data is not None and '_id' in data and data['_id'] is not None and data['_id'] != '':
        data['_id'] = str(data['_id'])


def deref(collection, _id):
    # result = collection.find_one({'_id': _id})
    result = find_one(collection, {'_id': _id})
    log.info('dereference: %s', _id)
    return result


# noinspection PyShadowingNames
def list_schema(schema_path=collection_path):
    for dirpath, dirnames, filenames in os.walk(schema_path):
        for fn in filenames:
            if not fn.endswith('.json'):
                continue
            yield dirpath, fn


# noinspection PyShadowingNames
def load_json(path, schema_path=collection_path):
    js = json.loads(file_as_string(os.path.join(schema_path, path)))
    return js


def preload_collection(db):
    for collection in ['tag', 'ingredient', 'recipe']:
        for path, fn in list_schema(schema_path=os.path.join(collection_path, collection)):
            log.info('> Loading json %s %s', path, fn)
            js = load_json(os.path.join(path, fn))
            if isinstance(js, list):
                log.info('< Skip json list %s' % fn)
                continue
            if 'type' not in js or js['type'] not in VALID_COLLECTION:
                raise Error.InvalidCollection(fn)
            replace.child(db, js)
            replace.tag(db, js)
            replace.ingredient(db, js)
            try:
                if '_id' in js:
                    del js['_id']
                db[js['type']].insert(js)
            except Exception as e:
                log.error('Error: Cannot load collection: %s\n\t%s' % (fn, e))


class qcache(object):
    _data = {}

    @classmethod
    def set(cls, key, value):
        cls._data[key] = value

    @classmethod
    def get(cls, key):
        return cls._data[key]

    @classmethod
    def exists(cls, key):
        if key in cls._data:
            return True
        return False


def _mk_key(mode, collection, query):
    key = u'%s/%s' % (mode, collection.name)
    key += ''.join([u'/%s/%s/' % (k, '%s' % query[k]) for k in sorted(query)])
    # if key[-1] == '/':
    #    key = key[:-1]
    log.info('key: %s' % key)
    return key


def find(collection, query):
    return [doc for doc in collection.find(query)]
    key = _mk_key(u'find', collection, query)
    if not qcache.exists(key):
        qcache.set(key, [doc for doc in collection.find(query)])
    return qcache.get(key)


def find_one(collection, query):
    return collection.find_one(query)
    key = _mk_key(u'find_one', collection, query)
    if not qcache.exists(key):
        qcache.set(key, collection.find_one(query))
    return qcache.get(key)


def client():
    uri = u'mongodb://%s' % conf.get('db.mongo', 'host')
    port = conf.get('db.mongo', 'port')
    if port is not None and port != '':
        port = int(port)
        uri = u'%s:%s' % (uri, port)
    log.info('Using uri: %s', uri)
    return MongoClient(uri)


_db_default = 'monu'


class open(object):
    """
    context manager for opening mango database
        - opening connection
        - closing connection

        ex:
            for open() as handle:
                handle.users.find_one({'name': 'admin'})
    """

    class Error(object):
        class ConnectionFail(Exception):
            pass

    def __init__(self, name=_db_default):
        self.name = name
        self.handle = None

    def __enter__(self):
        self.handle = client()
        if self.handle is None:
            raise self.Error.ConnectionFail()
        return self.handle[self.name]

    def __exit__(self, type, value, traceback):
        self.handle.close()


def remove_all(collection):
    collection.remove({})


if __name__ == '__main__':
    from time import time

    start_time = time()
    part_time = start_time


    def elapsed(msg=None):
        global start_time, part_time
        now = time()
        elapsed = part_time - start_time
        part_time = now
        if msg is not None:
            print('%s %s' % (elapsed, msg))


    elapsed('start')
    result = find_one(open(), 'recipe', {'name': 'sauce moutarde'})
    elapsed('deux')
    result = find_one(open(), 'recipe', {'name': 'sauce moutarde'})
    elapsed('trois')
    result = find_one(open(), 'recipe', {'name': 'sauce moutarde'})
    elapsed('quatre')
