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
