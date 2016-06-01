# -*- coding: utf-8 -*-

from bson.code import Code

CODE = {
    'sum': Code('function(key, values) {'
                ' var total = 0;'
                ' for(var i = 0; i < values.length; i++) {'
                '     total += values[i];'
                ' }'
                ' return total;'
                '}')
}


def tag(db, collection):
    m = Code('function () {'
             '   if (this.tag === undefined) {'
             '       return;'
             '   }'
             '   this.tag.forEach(function(z){'
             '       emit(z, 1);'
             '   });'
             '}')
    r = Code('function(key, values) {'
             ' var total = 0;'
             ' for(var i = 0; i < values.length; i++) {'
             '     total += values[i];'
             ' }'
             ' return total;'
             '}')
    return db[collection].map_reduce(m, r, 'result-' + collection)


def has_tag(collection, tag_list):
    tl = u'var tl=[%s];' % u','.join([u'"%s"' % t.encode('ascii') for t in tag_list])
    m = Code(u'function () {'
             u'   if (this.tag === undefined) {'
             u'       return;'
             u'   }' + tl +
             u' var doc = this;'
             u'   this.tag.forEach(function(z){'
             u'       for(var i = 0, c; i < tl.length, c=tl[i]; i++) {'
             u'              if (z.name && z.name == tl[i]) {'
             u'                  emit(doc._id, 1);'
             u'              }'
             u'       }'
             u'   });'
             u'}')

    return collection.map_reduce(m, CODE['sum'], 'result-has_tag-' + collection.name)


def has_ingredient(collection, ingredient_list):
    #print ', '.join([ repr(t) for t in ingredient_list])
    tl = u'var tl=[%s];' % u','.join([u'"%s"' % t.encode('ascii') for t in ingredient_list])
    m = Code(u'function () {'
             u'   if (this.ingredient === undefined) {'
             u'       return;'
             u'   }' + tl +
             u' var doc = this;'
             u'   this.ingredient.forEach(function(z){'
             u'       for(var i = 0, c; i < tl.length, c=tl[i]; i++) {'
             u'              if (z.name && z.name == tl[i]) {'
             u'                  emit(doc._id, 1);'
             u'              }'
             u'       }'
             u'   });'
             u'}')

    return collection.map_reduce(m, CODE['sum'], 'result-has_ingredient-' + collection.name)


if __name__ == '__main__':
    import monu.mdb.common as mdb

    searched = ['salade', 'dessert', 'huile']

    with mdb.open() as db:
        print('Recipe')
        for row in has_tag(db.recipe, searched).find():
            print row
        print('Ingredient')
        for row in has_tag(db.ingredient, searched).find():
            print row
