from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('user', 'password')

        self.assertEqual(user.username, 'user',
                         "The name of the user after creation does not equal the constructor argument.")

        self.assertEqual(user.password, 'password',
                         "The password of the user after creation does not equal the constructor argument.")
