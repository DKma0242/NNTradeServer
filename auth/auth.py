import hashlib
from collections import OrderedDict
from functools import wraps
from django.http import QueryDict
from erron import erron
from models import AuthKey


def get_dict_md5(data, secret_key):
    sorted_data = OrderedDict(sorted(data.iteritems(), key=lambda d: d[0]))
    sorted_data['secret'] = secret_key
    text = '&'.join([key + '=' + value for key, value in data.items()])
    return hashlib.md5(text).hexdigest()


def authenticate(view):
    @wraps(view)
    def wrapper(request):
        if request.method == 'GET':
            data = request.GET
        elif request.method == 'POST':
            data = request.POST
        elif request.method == 'PUT':
            request.PUT = QueryDict(request.body)
            data = request.PUT
        elif request.method == 'DELETE':
            request.DELETE = QueryDict(request.body)
            data = request.DELETE
        else:
            return erron.response_with_erron(erron.ERRON_INVALID_REQUEST_METHOD)
        if 'key' not in data.keys() or 'secret' not in data.keys():
            return erron.response_with_erron(erron.ERROR_MISSING_PARAMETER)
        key = data['key']
        auth = AuthKey.objects.get(key=key)
        if auth is None:
            return erron.response_with_erron(erron.ERROR_AUTHENTICATE)
        secret_key = auth.secret
        secret_md5 = get_dict_md5(data, secret_key)
        if secret_md5 != data['secret']:
            return erron.response_with_erron(erron.ERROR_AUTHENTICATE)
        view(request)
    return wrapper