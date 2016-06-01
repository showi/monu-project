# -*- coding: utf-8 -*-

from monu.logger import getLogger
log = getLogger('mdb.replace')


class insert(object):
    @classmethod
    def tag(cls, db, data):
        from monu.mdb import common as mdb
        data['type'] = 'tag'
        result = mdb.find_one(db.tag, {'name': data['name']})
        print('find one: %s' % result)
        if result is None:
            _id = db.tag.insert(data)
            result = mdb.find_one(db.tag, {'_id': _id})
            log.debug('Tag %s inserted with id: %s', data['name'], result['_id'])
        return result

    @classmethod
    def ingredient(cls, db, data):
        from monu.mdb import common as mdb
        data['type'] = 'ingredient'
        result = mdb.find_one(db.ingredient, {'name': data['name']})
        if result is None:
            _id = db.ingredient.insert(data)
            result = db.ingredient.find_one({'_id': _id})
            log.debug('Ingredient %s inserted with id: %s', result['name'], _id)
        return result

    @classmethod
    def recipe(cls, db, data):
        from monu.mdb import common as mdb
        data['type'] = 'recipe'
        result = mdb.find_one(db.recipe, {'name': data['name']})
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
            log.info('Recipe %s inserted with id: %s\n', result['name'], _id)
        return result
