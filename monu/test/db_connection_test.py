# -*- coding: utf-8 -*-

import unittest

from monu import mdb

data = {
    'tag': {
        'type': 'tag',
        'name': 'test',
        'lang': 'fr_fr'
    }
}


class TestDb(unittest.TestCase):
    db_name = 'monu'

    def setUp(self):
        pass

    def test_open(self):
        with mdb.util.open() as handle:
            self.assertIsNotNone(handle)

    def test_insert_tag(self):
        with mdb.util.open() as handle:
            tag = mdb.insert.tag(handle.tag, data['tag'])
            self.assertIsNotNone(tag)
            print('tag: %s' % (tag))
            for doc in mdb.list.tag(handle):
                print doc

    def ktest_remove_tag(self):
        with mdb.util.open(self.db_name) as handle:
            tag = mdb.insert.tag(handle.tag, data['tag'])
            print('inserted tag %s' % tag)
            res = handle.tag.delete_many({'_id': tag['_id']})
            self.assertEqual(res.deleted_count, 1)

    def test_list(self):
        with mdb.util.open(self.db_name) as handle:
            for collection in ['tag', 'ingredient', 'recipe']:
                for doc in getattr(mdb.list, collection)(handle):
                    print doc

    def test_mapreduce(self):
        from monu.mdb import redux
        with mdb.util.open(self.db_name) as handle:
            for tl in [['entrée', ], ['plat', ], ['desser', ], ['citron', 'rhum']]:
                print "> recipe has_tag %s" % tl
                for doc in redux.has_tag(handle.recipe, tl).find():
                    print ' - %s' % mdb.util.find_one(handle.recipe, doc['_id'])['name']

    def dtest_search_tag(self):
        with mdb.util.open(self.db_name) as handle:
            tag = mdb.insert.tag(handle.tag, data['tag'])
            print('inserted tag %s' % tag)
            print('searching tag with id %s' % repr(tag['_id']))
            tag_found = handle.tag.find_one({'_id': str(tag['_id'])})
            print('tag found: %s' % tag_found)

            tag_found = mdb.util.find_one(handle.tag, {'_id': tag['_id']})
            print('tag found: %s' % tag_found)
            self.assertIsNotNone(tag_found)

            # def test_upper(self):
            #     self.assertEqual('foo'.upper(), 'FOO')
            #
            # def test_isupper(self):
            #     self.assertTrue('FOO'.isupper())
            #     self.assertFalse('Foo'.isupper())
            #
            # def test_split(self):
            #     s = 'hello world'
            #     self.assertEqual(s.split(), ['hello', 'world'])
            #     # check that s.split fails when the separator is not a string
            #     with self.assertRaises(TypeError):
            #         s.split(2)


if __name__ == '__main__':
    unittest.main()
