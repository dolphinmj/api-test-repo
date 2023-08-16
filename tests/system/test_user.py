from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(UserModel.find_by_username('test'))

                response = client.post('/register', json={'username': 'test', 'password': 'password'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'User created successfully.'})

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': 'password'})
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': 'password'}),
                                            headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': 'password'})

                response = client.post('/register', json={'username': 'test', 'password': 'password'})
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "A user with username 'test' already exists."})
