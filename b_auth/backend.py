import copy
from models import User
import utils

auth_request = {
    "methods": "password",
    "password": {
        "user": {
            "name": "",
            "password": "",
            "encryption": ""
        }
    }
}


class Backend(object):
    def authenticate(self, username=None, password=None):
        return utils.is_authentication(name=username, password=password)

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
