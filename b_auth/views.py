from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponse
from utils import is_authentication
from utils import is_permission
from models import Resource
import json
from django.contrib.auth.decorators import login_required


# Create your views here.

# app = {
#     "methods": "password",
#     "password": {
#         "user": {
#             "name": "admin",
#             "password": "devstacker",
#             "encryption": 'md5'
#         }
#     }
# }


def get_resource(name, type, extra=None):
    try:
        resource = Resource.objects.get(name=name)
    except Resource.DoesNotExist:
        resource = Resource()
        resource.name = name
        resource.type = type
        resource.extra = extra
        resource.save()
    return resource


class Auth(View):
    def get(self, request):
        print request.user.is_authenticated()
        resource_name = "{}.{}".format(request.resolver_match.view_name, "get")
        get_resource(name=resource_name, type="public")
        return JsonResponse({"aa": "cc", "cc": 123})

    def post(self, request):
        resource_name = "{}.{}".format(request.resolver_match.view_name, "get")
        get_resource(name=resource_name, type="public")
        data = json.loads(request.body)
        return JsonResponse(is_authentication(data))


class Permission(View):
    def get(self, request):
        resource_name = "{}.{}".format(request.resolver_match.view_name, "get")
        get_resource(name=resource_name, type="admin")
        return JsonResponse({"aa": "cc", "cc": 123})

    def post(self, request):
        resource_name = "{}.{}".format(request.resolver_match.view_name, "post")
        get_resource(name=resource_name, type="public")
        return JsonResponse({"permission": is_permission(request.user, resource_name)})


class ResourceList(View):
    def get(self, request):
        resource_name = "{}.{}".format(request.resolver_match.view_name, "get")
        get_resource(name=resource_name, type="public")
        return HttpResponse(
            json.dumps([{"id": i.id.hex, "name": i.name, "type": i.type} for i in Resource.objects.all()]))


class Login(View):
    def get(self, request):
        name = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=name, password=password)
        if user:
            login(request, user)
            print "success"
        else:
            return HttpResponse("authenticate faild")
        return HttpResponse(json.dumps({"name": name, "password": password}))


class Logout(View):
    def get(self, request):
        # user = request.user.name
        logout(request)
        print "logout success"
        return HttpResponse("{} logout".format(''))
