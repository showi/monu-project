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
    tl = 'var tl=[%s];' % ','.join(['"%s"' % t for t in tag_list])
    m = Code('function () {'
             '   if (this.tag === undefined) {'
             '       return;'
             '   }'
                + tl +
             ' var doc = this;'
             '   this.tag.forEach(function(z){'
             '       for(var i = 0, c; i < tl.length, c=tl[i]; i++) {'
             '              if (z.name && z.name == tl[i]) {'
             '                  emit(doc._id, 1);'
             '              }'
             '       }'
             '   });'
             '}')

    return collection.map_reduce(m, CODE['sum'], 'result-has_tag-' + collection.name)



def has_ingredient(collection, ingredient_list):
    tl = 'var tl=[%s];' % ','.join(['"%s"' % t for t in ingredient_list])
    m = Code('function () {'
             '   if (this.ingredient === undefined) {'
             '       return;'
             '   }'
                + tl +
             ' var doc = this;'
             '   this.ingredient.forEach(function(z){'
             '       for(var i = 0, c; i < tl.length, c=tl[i]; i++) {'
             '              if (z.name && z.name == tl[i]) {'
             '                  emit(doc._id, 1);'
             '              }'
             '       }'
             '   });'
             '}')

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