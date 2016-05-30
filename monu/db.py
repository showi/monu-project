# -*- coding: utf-8 -*-
from pymongo import MongoClient
import monu
from monu import logger

print('base_path: %s', monu.base_path)
from util import file_as_string
import json
from monu.mdb.redux import mr_tag
from monu.mdb.common import load_json

log = logger.getLogger('mongo')


class Error(object):
    class NameAlreadyInCollection(Exception):
        pass


def exists(collection, name):
    return collection.find_one({'name': name})


import uuid

from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def insert_tag(db, data):
    print('insert %s', data)
    data['type'] = 'tag'
    result = db.tag.find_one({'name': data['name']})
    if result is None:
        print('insert tag data %s' % data)
        _id = db.tag.insert(data)
        result = db.tag.find_one({'_id': _id})
        print('result: %s' % result)
        log.debug('Tag %s inserted with id: %s', data['name'], result['_id'])
    return result


def search_and_replace_tag(db, data):
    if 'tag' not in data or data['tag'] is None:
        return
    newtag = []
    for tag in data['tag']:
        if isinstance(tag, basestring):
            newtag.append(insert_tag(db, tag))
        else:
            newtag.append(tag)
    data['tag'] = newtag


def astrid(data):
    if data is not None and '_id' in data and data['_id'] is not None and data['_id'] != '':
        data['_id'] = str(data['_id'])


def deref(collection, _id):
    result = collection.find_one({'_id': _id})
    return result


def search_and_replace_ingredient(db, data):
    if 'ingredient' not in data or data['ingredient'] is None:
        return
    newingredient = []
    for ingredient in data['ingredient']:
        if isinstance(tag, basestring):
            newingredient.append(insert_tag(db, tag))
        else:
            newingredient.append(tag)
    data['tag'] = newingredient


def insert_ingredient(db, data):
    data['type'] = 'ingredient'
    result = db.ingredient.find_one({'name': data['name']})
    if result is None:
        _id = db.ingredient.insert(data)
        log.info('Ingredient id ? %r', _id)
        result = db.ingredient.find_one({'_id': _id})
        log.debug('Ingredient %s inserted with id: %s', result['name'], _id)
    return result


def insert_recipe(db, data):
    data['type'] = 'recipe'
    result = db.recipe.find_one({'name': data['name']})
    if result is None:
        print('data: %s' % data)
        for r in data['ingredient']:
            if isinstance(r['name'], basestring):
                nr = {
                    'ref': 'ingredient',
                    'id': insert_ingredient(db, {'name': r['name']})['_id']
                }
                r['name'] = nr
        nt = []
        for tag in data['tag']:
            if tag is None or tag == '':
                continue
            if isinstance(tag, basestring):
                newtag = {
                    'ref': 'tag',
                    'id': str(insert_tag(db, {'name': tag})['_id'])
                }
                log.info('newtag %s' % newtag)
                nt.append(newtag)
            else:
                nt.append(tag)
        data['tag'] = nt
        _id = db.recipe.insert(data)
        result = db.recipe.find_one({'_id': _id})
        log.info('Recipe %s inserted with id: %s\n\t%s', result['name'], _id, result)
    return result


def insert(collection, name, language='fr', tag=None, data={}):
    name = name.strip().lower()
    data['_id'] = str(uuid.uuid4())
    data['language'] = language
    data['name'] = name
    data['tag'] = tag
    if exists(collection, name):
        raise Error.NameAlreadyInCollection(name)
    try:
        return collection.insert(data)
    except Exception as e:
        print('Error: Fail inserting <<%s>> with error:\n\t%s\n' % (name, e))
    return None


def is_id(value):
    if len(value) != 36:
        return False
    if value[8] == value[13] == value[23] == '-':
        return True
    return False


def find(collection, key='name', value=None):
    if value is not None:
        doc = collection.find_one({key: value})
        if doc is not None:
            yield doc
    else:
        for doc in collection.find():
            yield doc


def remove_all(collection):
    collection.remove({})


def client(uri='mongodb://db:27017'):
    return MongoClient(uri)


def open(name='monu'):
    return client()[name]


def id_from_name(handle, name):
    return handle.find_one({'name': name})


def name_from_id(handle, _id):
    return handle.find_one({'_id': _id})


if __name__ == '__main__':
    import os
    import sys

    client = client()
    db = client.monu
    ingredient = db.ingredient
    recipe = db.recipe
    tag = db.tag

    # print('Tag recipe')
    # for doc in mr_tag(db, 'recipe').find():
    #     print doc
    # print('Tag ingredient')
    # for doc in mr_tag(db, 'ingredient').find():
    #     print doc
    # sys.exit(0)
    remove_all(ingredient)
    remove_all(tag)
    remove_all(recipe)

    for schema in load_json('dataset.json'):
        del schema['_id']
        if schema['type'] == 'recipe':
            insert_recipe(db, schema)
        elif schema['type'] == 'ingredient':
            insert_ingredient(db, schema)
        elif schema['type'] == 'tag':
            insert_tag(db, schema)
    sys.exit(0)


    def sprint(txt):
        print(txt.encode('ascii', errors='ignore'))


    def ift(name):
        t = id_from_name(tag, name)
        if t is None:
            sprint(u'Inserting tag %s' % name)
            return insert(tag, name)
        return t['_id']


    def ifi(name):
        t = id_from_name(ingredient, name)
        if t is None:
            sprint(u'Inserting ingredient %s' % name)
            return insert(ingredient, name)
        return t['_id']


    remove_all(recipe)
    name = 'sauce aux agrumes'
    if not exists(recipe, name):
        insert(recipe, name,
               tag=[ift(u'sauce'), ift('poisson'), ift('beurre'), ift('agrume'), ift('citron'), ift('pamplemousse')],
               data={
                   'note': 'Vous pouvrez remplacer le citron par du pamplemousse, varier les agrumes ou les mélanger.',
                   'ingredient': [[ifi(u'beurre'), '50', 'g'], [ifi(u'citron jaune'), '1', 'pc'],
                                  [ifi(u'citron vert'), '1', 'pc'], [ifi(u'échalotte'), '1', 'pc']],
                   'step': [
                       {'text': u'Peler et émincer échalotte', 'title': u'Emincer', 'duration': 60},
                       {
                           'text': u'Faire fondre la moitié de la quantitée de beurre, faire revenir les échalotes dans le beurre sans colorer',
                           'title': u'L\'échalote', 'duration': 30},
                       {'text': u'Récupérer du zeste sur les agrumes, presser les les agrumes', 'title': u'Agrumes',
                        'duration': 90}

                   ]
               })

    name = 'compote de pommes sèche'
    if not exists(recipe, name):
        insert(recipe, name, tag=[ift(u'pomme'), ift('compote'), ift('dessert')], data={
            'ingredient': [[ifi(u'pomme'), '5', 'pc'], [ifi(u'rhum'), '1', 'cas'], [ifi(u'citron'), '0.5', 'pc'],
                           [ifi(u'sucre'), '25', 'g']],
            'step': [
                {'text': u'Peler et couper les pommes en quartier', 'title': u'Pélé et couper', 'duration': 500},
                {'text': u'Récupérer le jus d\'un demi citron', 'title': u'Jus de citron', 'duration': 60},
                {'text': u'Faire revenir les pommes 5mn avec le sucre à fau moyen (à vif), pour qu\'elles colorent',
                 'title': u'De la couleur', 'duration': 500},
                {'text': u'Laisser mijoter 10mn à feu moyen couvert', 'title': u'Mijote', 'duration': 600},
                {'text': u'Ecraser les pommes au presse purée', 'title': u'Ecrase un peu', 'duration': 600},
                {'text': u'Ajouter le jus du demi citron et laisser réduire 5mn', 'title': u'Réduire', 'duration': 600},
                {
                    'text': u'Laisser refroidir en enlevant le couvercle, puis consommer tiède ou mettre au réfrigérateur pour le lendemain',
                    'title': u'Finir', 'duration': 500},
            ]
        })

    for doc in find(ingredient):
        print(doc['name'].encode('utf8', errors="replace"))
    for doc in find(recipe):
        print(doc['name'].encode('utf8', errors="replace"))

    s = 'a6aac969-0718-4163-a6db-9021b4179bb4'
    print('is id %s: %s' % (s, is_id(s)))
