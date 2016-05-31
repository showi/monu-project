from monu.logger import getLogger
from monu.mdb.insert import insert

log = getLogger('mdb.replace')


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
        new_ingredient = []
        for ingredient in data['ingredient']:
            if 'name' in ingredient and isinstance(ingredient['name'], basestring):
                new_ingredient.append(insert.ingredient(db, {'name': ingredient['name']}))
            else:
                new_ingredient.append(ingredient)
        data['ingredient'] = new_ingredient

    @classmethod
    def tag(cls, db, data):
        if 'tag' not in data or data['tag'] is None:
            return
        newtag = []
        for tag in data['tag']:
            if isinstance(tag, basestring):
                nt = insert.tag(db, {'name': tag})
                newtag.append(nt)
            else:
                newtag.append(tag)
        data['tag'] = newtag
