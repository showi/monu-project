from bson.code import Code


def mr_tag(db, collection):
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

def mr_tagged_with(collection, tag_list):
    tl = 'var tl=[%s];' % ','.join(['"%s"' % t for t in tag_list])
    print('Array: %s' % tl)
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


    r = Code('function(key, values) {'
         ' var total = 0;'
         ' for(var i = 0; i < values.length; i++) {'
         '     total += values[i];'
         ' }'
         ' return total;'
         '}')
    return collection.map_reduce(m, r, 'result-' + collection.name)

if __name__ == '__main__':
    import monu.mdb.common as mdb
    searched = ['salade', 'dessert', 'huile']

    with mdb.open() as db:
        print('Recipe')
        for row in mr_tagged_with(db.recipe, searched).find():
            print row
        print('Ingredient')
        for row in mr_tagged_with(db.ingredient, searched).find():
            print row