from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'),
                              "Found an store with name {}, but expected not to.".format(store.name))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'),
                                 "Did not find store with name{}, but expected to after save to db".format(store.name))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'),
                          "Found store with name {}, but didn't expect to after deleting from db".format(store.name))

    def test_create_store_items_item(self):
        store = StoreModel('test')
        self.assertListEqual(store.items.all(), [],
                             "The new store's items length is not 0 even though no items were added")

    def test_store_item_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test item', 20.12, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1,
                             "The new store's item was not added to items list")
            self.assertEqual(store.items.first().name, "test item",
                             "Name of item in store object doesn't match created item")

    def test_json(self):
        with self.app_context():
            store = StoreModel('test_store')
            store.save_to_db()

            expected = {
                'id': 1,
                'name': 'test_store',
                'items': []
            }

            self.assertDictEqual(store.json(), expected,
                                 "JSON output of store doesn't match expected")

    def test_json_with_items(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test item', 20.12, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1,
                             "The new store's item was not added to items list")
            self.assertEqual(store.items.first().name, "test item",
                             "Name of item in store object doesn't match created item")

            expected = {
                'id': 1,
                'name': 'test_store',
                'items': [{
                    'name': 'test item',
                    'price': 20.12,
                    'store_id': 1
                }]
            }

            self.assertDictEqual(store.json(), expected,
                                 "JSON output of store doesn't match expected, received {}, expected {}".format(
                                     store.json(), expected))
