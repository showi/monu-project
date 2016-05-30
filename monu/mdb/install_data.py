if __name__ == '__main__':
    from monu.mdb.common import preload_collection, open, remove_all

    db = open()
    remove_all(db.tag)
    remove_all(db.ingredient)
    remove_all(db.recipe)
    preload_collection(open())
