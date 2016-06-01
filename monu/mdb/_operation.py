class Operation(object):
    @classmethod
    def open(cls):
        from monu import mdb
        return mdb.open()