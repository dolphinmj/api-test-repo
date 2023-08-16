from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('user1', 'password').save_to_db()

                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'user1', 'password': 'password'}),
                                            headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_response.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                self.assertIsNone(ItemModel.find_by_name('test'))

                response = client.post('/item/{}'.format('test'), json={'price': '19.99', 'store_id': '1'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name('test'))
                self.assertDictEqual(json.loads(response.data),
                                     {'name': 'test', 'price': 19.99, 'store_id': 1})

    def test_create_item_duplicate(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item1', '1.23', 1).save_to_db()

                response = client.post('/item/{}'.format('test_item1'), json={'price': '19.99', 'store_id': '1'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "An item with name 'test_item1' already exists."})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item1', '1.23', 1).save_to_db()

                delete_response = client.delete('/item/{}'.format('test_item1'))

                self.assertIsNone(ItemModel.find_by_name('test_item1'))
                self.assertEqual(len(delete_response.data), 0)
                self.assertEqual(delete_response.status_code, 204)

    def test_delete_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                delete_response = client.delete('/item/{}'.format('test_item1'))

                self.assertDictEqual(json.loads(delete_response.data),
                                     {'message': 'Item not found for deletion'})
                self.assertEqual(delete_response.status_code, 404)

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                response = client.put('/item/{}'.format('test_item1'), json={'price': '19.99', 'store_id': '1'})

                self.assertEqual(response.status_code, 201)
                self.assertEqual(ItemModel.find_by_name('test_item1').price, 19.99)
                self.assertDictEqual(json.loads(response.data),
                                     {'name': 'test_item1', 'price': 19.99, 'store_id': 1})

    def test_put_item_update(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item1', '19.99', 1).save_to_db()

                response = client.put('/item/{}'.format('test_item1'), json={'price': '421.21', 'store_id': '1'})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test_item1').price, 421.21)
                self.assertDictEqual(json.loads(response.data),
                                     {'name': 'test_item1', 'price': 421.21, 'store_id': 1})

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/{}'.format('test_item1'))

                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Authorization Required: Request does not contain an access token'})
                self.assertEqual(response.status_code, 401)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test_item', '19.99', 1).save_to_db()

                response = client.get('/item/{}'.format('test_item'),
                                      headers={'Authorization': self.access_token})

                expected = {
                    'name': 'test_item',
                    'price': 19.99,
                    'store_id': 1
                }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/{}'.format('test_item'),
                                      headers={'Authorization': self.access_token})
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Item not found'})
                self.assertEqual(response.status_code, 404)

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test1').save_to_db()
                StoreModel('test2').save_to_db()
                StoreModel('test3').save_to_db()

                ItemModel('test_item1', '19.99', 1).save_to_db()
                ItemModel('test_item2', '1.99', 1).save_to_db()
                ItemModel('test_item3', '0.36', 2).save_to_db()
                ItemModel('test_item4', '23.99', 3).save_to_db()
                response = client.get('/items')

                expected = {
                    'items': [
                        {
                            'name': 'test_item1',
                            'price': 19.99,
                            'store_id': 1
                        },
                        {
                            'name': 'test_item2',
                            'price': 1.99,
                            'store_id': 1
                        },
                        {
                            'name': 'test_item3',
                            'price': 0.36,
                            'store_id': 2
                        },
                        {
                            'name': 'test_item4',
                            'price': 23.99,
                            'store_id': 3
                        }
                    ]
                }

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), expected)

    def test_item_list_empty(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/items')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'items': []})
