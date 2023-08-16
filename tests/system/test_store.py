from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('test'))

                response = client.post('/store/{}'.format('test'))

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'test', 'items': []})

    def test_create_store_duplicate(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/{}'.format('test'))
                response = client.post('/store/{}'.format('test'))

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "A store with name 'test' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                delete_response = client.delete('/store/{}'.format('test'))

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertEqual(len(delete_response.data), 0)
                self.assertEqual(delete_response.status_code, 204)

    def test_delete_nonexistent_store(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('test'))
                delete_response = client.delete('/store/{}'.format('test'))

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertEqual(delete_response.status_code, 404)
                self.assertDictEqual(json.loads(delete_response.data),
                                     {'message': "No store found to delete."})

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                response = client.get('/store/{}'.format('test'))

                expected = {
                    'id': 1,
                    'name': 'test',
                    'items': []
                }
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_find_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', '19.99', 1).save_to_db()

                response = client.get('/store/{}'.format('test'))

                expected = {
                    'id': 1,
                    'name': 'test',
                    'items': [{
                        'name': 'test_item',
                        'price': 19.99,
                        'store_id': 1
                    }]
                }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/{}'.format('test'))

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Store not found'})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test1').save_to_db()
                StoreModel('test2').save_to_db()

                response = client.get('/stores')

                expected = {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'test1',
                            'items': []
                        },
                        {
                            'id': 2,
                            'name': 'test2',
                            'items': []
                        }
                    ]
                }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test1').save_to_db()
                ItemModel('test_item1', '19.99', 1).save_to_db()
                ItemModel('test_item2', '0.34', 1).save_to_db()
                StoreModel('test2').save_to_db()

                response = client.get('/stores')

                expected = {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'test1',
                            'items': [{
                                'name': 'test_item1',
                                'price': 19.99,
                                'store_id': 1
                            },
                                {
                                'name': 'test_item2',
                                'price': 0.34,
                                'store_id': 1
                            }]
                        },
                        {
                            'id': 2,
                            'name': 'test2',
                            'items': []
                        }
                    ]
                }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_store_list_empty(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/stores')

                expected = {
                    'stores': []
                }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)