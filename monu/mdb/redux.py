# -*- coding: utf-8 -*-

from bson.code import Code
from monu.logger import getLogger

log = getLogger('mdb.redux')

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


def has_tag(collection, tag_list, key='_id'):
    tl = u'var tl=[%s];' % u','.join([u'"%s"' % t.encode('ascii', errors='ignore') for t in tag_list])
    m = Code(u'function () {'
             u'   if (this.tag === undefined) {'
             u'       return;'
             u'   }' + tl +
             u' var doc = this;'
             u'   this.tag.forEach(function(z){'
             u'       for(var i = 0, c; i < tl.length, c=tl[i]; i++) {'
             u'              if (z["'+key+'"] && z["'+key+'"] == tl[i]) {'
             u'                  emit(doc._id, 1);'
             u'              }'
             u'       }'
             u'   });'
             u'}')

    return collection.map_reduce(m, CODE['sum'], 'result-has_tag-' + collection.name)


def has_ingredient(collection, ingredient_list, key='_id'):
    name = 'result-has_ingredient-%s' % ','.join(ingredient_list)
    ingredient_list = u','.join([u'"%s"' % t.encode('ascii', errors='ignore') for t in ingredient_list])
    tl = u'var tl=[%s];' % ingredient_list
    m = Code(u'function () {'
             u'   if (this.ingredient === undefined) {'
             u'       return;'
             u'   }' + tl +
             u' var doc = this;'
             u'   this.ingredient.forEach(function(z){'
             u'       for(var i = 0, c; i < tl.length, c=tl[i]; i++) {'
             u'              if (z["' + key +u'"] && z["' + key + u'"] == tl[i]) {'
             u'                  emit(doc._id, 1);'
             u'              }'
             u'       }'
             u'   });'
             u'}')

    return collection.map_reduce(m, CODE['sum'], name)
