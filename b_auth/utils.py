import copy
import define
import json
from .models import Resource
from .models import Role
from .models import RoleResource
from .models import User

# Create your views here.
__all__ = ["is_authentication", "is_permission"]

auth_request = {
    "methods": "password",
    "password": {
        "user": {
            "name": "admin",
            "password": "devstacker",
            "encryption": 'md5'
        }
    }
}

permission_request = {
    "resource": {
        "name": "/permission/post"
    }
}

response = {
    'ok': False,
    "msg": '',
    'data': {},
}


class DictToObject(object):
    def __init__(self, dict_object):
        for k, v in dict_object.iteritems():
            setattr(self, k, v)


class Storage(dict):
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)

    def __getattr__(self, key):
        return self.get(key, None)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]


class AuthBase(object):
    @staticmethod
    def _passwd(user):
        resp = copy.copy(response)
        try:
            auth_user = User.objects.get(name=user['name'])
        except Exception:
            # The user does not exist
            resp['msg'] = "The user does not exist."
            return resp
        if not user.get('encryption', None):
            if auth_user.password == user.get("password"):
                resp['ok'] = True
                resp['data'] = {
                    "id": auth_user.id.hex,
                    "name": auth_user.name,
                    "role": auth_user.role.name,
                }
                if auth_user.extra:
                    resp['data'].update(json.loads(auth_user.extra))
                return resp
            # Failed user authentication
            resp['msg'] = "Failed user authentication."
            return resp
        if user.get('encryption') == define.MD5:
            return resp

    @staticmethod
    def get_user(id=None, name=None):
        if id:
            return User.objects.get(id=id)
        elif name:
            return User.objects.get(name=name)

    @staticmethod
    def api_authentication(data):
        if data.get("methods") == 'password' and data.get("password"):
            return AuthBase._passwd(data.get("password").get("user"))

    @staticmethod
    def is_authentication(name, password):
        try:
            user = User.objects.get(name=name, password=password)
        except Exception:
            user = None
        return user

    @staticmethod
    def _permission(user, resource_name):
        try:
            resource = Resource.objects.get(name=resource_name)
        except Resource.DoesNotExist:
            # The resource does not exist
            return False, "The resource does not exist."
        if resource.type == define.PUBLIC:
            return True, ""
        if not user:
            # The user not login
            return False, "The user not login."
        if user.role == define.ADMIN:
            return True, ""
        role = Role.objects.get(name=user.role)
        try:
            RoleResource.objects.get(role=role, resource=resource)
            return True, ""
        except Exception:
            # The user has no permissions
            return False, "The user has no permissions."

    @staticmethod
    def api_permission(user, data):
        resp = copy.copy(response)
        resp["ok"], resp["msg"] = AuthBase._permission(user, data["resource"]["name"])
        return resp

    @staticmethod
    def is_permission(user=None, resource_name=None):
        status, msg = AuthBase._permission(user, resource_name)
        return status


def is_authentication(name, password):
    return AuthBase.is_authentication(name, password)


def api_authentication(data):
    return AuthBase.api_authentication(data)


def is_permission(user=None, resource_name=None):
    return AuthBase.is_permission(user, resource_name)


def get_user(id=None, name=None):
    return AuthBase.get_user(id, name)
