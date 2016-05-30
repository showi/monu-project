from monu.logger import getLogger

log = getLogger('mdb.replace')


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
