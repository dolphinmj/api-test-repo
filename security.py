import hmac
from models.user import UserModel


def authenticate(username, password):
    """
    Function that gets called when a user calls the /auth endpoint
    with their username & password.
    :param username: User's username in string format
    :param password: User's unencrypted password in string format.
    :return: A UserModel object if the authentication was successful, None otherwise.
    """

    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user


def identity(payload):
    """
    function that gets called when user has already authenticated and Flask-JWT
    verified their authorization header is correct
    :param payload: A dictionary with 'identity' key, which is the user id
    :return: a UserModel object
    """

    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
