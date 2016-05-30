import os
import json
import monu
from monu.util import file_as_string
from monu.logger import getLogger
from pymongo import MongoClient
from bson import ObjectId
from monu.conf import conf

log = getLogger('monu.mdb.common')

schema_path = os.path.join(monu.base_path, 'monu', 'data', 'schema')
collection_path = os.path.join(schema_path, 'collection')

VALID_COLLECTION = [u'ingredient', u'recipe', u'tag']


class Error(object):
    class InvalidCollection(Exception):
        pass


class Base(object):
    pass


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


encoder = JSONEncoder()


def astrid(data):
    if data is not None and '_id' in data and data['_id'] is not None and data['_id'] != '':
        data['_id'] = str(data['_id'])


def deref(collection, _id):
    log.info('DeRef %s', _id)
    result = collection.find_one({'_id': _id})
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


class insert(object):
    @classmethod
    def tag(cls, db, data):
        data['type'] = 'tag'
        result = db.tag.find_one({'name': data['name']})
        if result is None:
            _id = db.tag.insert(data)
            result = db.tag.find_one({'_id': _id})
            log.debug('Tag %s inserted with id: %s', data['name'], result['_id'])
        return result

    @classmethod
    def ingredient(cls, db, data):
        data['type'] = 'ingredient'
        result = db.ingredient.find_one({'name': data['name']})
        if result is None:
            _id = db.ingredient.insert(data)
            result = db.ingredient.find_one({'_id': _id})
            log.debug('Ingredient %s inserted with id: %s', result['name'], _id)
        return result

    @classmethod
    def recipe(cls, db, data):
        data['type'] = 'recipe'
        result = db.recipe.find_one({'name': data['name']})
        if result is None:
            ni = []
            for r in data['ingredient']:
                if r is None or r == '':
                    continue
                if isinstance(r['name'], basestring):
                    nr = {
                        'ref': 'ingredient',
                        '_id': insert.ingredient(db, {'name': r['name']})['_id']
                    }
                    ni.append(nr)
            data['ingredient'] = ni
            nt = []
            for tag in data['tag']:
                if tag is None or tag == '':
                    continue
                if isinstance(tag, basestring):
                    newtag = {
                        'ref': 'tag',
                        '_id': insert.tag(db, {'name': tag})['_id']
                    }
                    nt.append(newtag)
                else:
                    nt.append(tag)
            data['tag'] = nt
            _id = db.recipe.insert(data)
            result = db.recipe.find_one({'_id': _id})
            log.info('Recipe %s inserted with id: %s\n\t%s', result['name'], _id, result)
        return result


class replace(object):
    """
    Modify raw json for mongo insert
    """

    @classmethod
    def child(cls, db, js):
        if 'child' not in js or not isinstance(js['child'], list):
            return False
        for child in js['child']:
            recipe = insert.recipe(db, child)
        return True

    @classmethod
    def recipe(cls, db, js):
        pass

    @classmethod
    def ingredient(cls, db, data):
        if 'ingredient' not in data or data['ingredient'] is None:
            return
        newingredient = []
        for ingredient in data['ingredient']:
            if 'name' in ingredient and isinstance(ingredient['name'], basestring):
                newingredient.append(insert.ingredient(db, {'name': ingredient['name']}))
            else:
                newingredient.append(ingredient)
        data['ingredient'] = newingredient
        log.info('New ingredient %s', newingredient)

    @classmethod
    def tag(cls, db, data):
        if 'tag' not in data or data['tag'] is None:
            return
        newtag = []
        for tag in data['tag']:
            if isinstance(tag, basestring):
                nt = insert.tag(db, {'name': tag})
                log.info('nt: %s', nt)
                newtag.append(nt)
            else:
                newtag.append(tag)
        data['tag'] = newtag
        log.info('New tag %s' % newtag)


def preload_collection(db):
    for path, fn in list_schema(schema_path=collection_path):
        log.info('> Loading json %s %s', path, fn)
        js = load_json(os.path.join(path, fn))
        if isinstance(js, list):
            log.info('< Skip list %s')
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


def client():
    uri = u'mongodb://%s' % conf.get('db.mongo', 'host')
    port = conf.get('db.mongo', 'port')
    if port is not None and port != '':
        port = int(port)
        uri = u'%s:%s' % (uri, port)
    log.info('Using uri: %s', uri)
    return MongoClient(uri)


def open(name='monu'):
    return client()[name]


def remove_all(collection):
    collection.remove({})


if __name__ == '__main__':
    for sch in list_schema():
        print sch

    for sch in list_schema(schema_path=schema_path):
        print sch

    preload_collection(open())
