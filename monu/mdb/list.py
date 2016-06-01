class list(object):
    @classmethod
    def tag(cls, db, query={}):
        for doc in db.tag.find(query):
            yield doc

    @classmethod
    def ingredient(cls, db, query={}):
        for doc in db.ingredient.find(query):
            yield doc

    @classmethod
    def recipe(cls, db, query={}):
        for doc in db.recipe.find(query):
            yield doc
