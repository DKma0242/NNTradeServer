import ast
import hashlib
import operator
from collections import OrderedDict
from functools import wraps
from erron import errno
from account.models import UserToken
from models import AuthKey


def get_dict_md5(data, secret_key):
    sorted_data = data.copy()
    sorted_data['secret'] = secret_key
    sorted_data = OrderedDict(sorted(sorted_data.items(), key=operator.itemgetter(0)))
    text = '&'.join([key + '=' + value for key, value in sorted_data.items()])
    return hashlib.md5(text).hexdigest()


def init_rest(request):
    if not hasattr(request, 'data'):
        if request.method == 'GET':
            request.data = request.GET
        elif request.method == 'POST':
            request.data = request.POST
        elif request.method == 'PUT':
            request.PUT = ast.literal_eval(request.body)
            request.data = request.PUT
        elif request.method == 'DELETE':
            request.DELETE = ast.literal_eval(request.body)
            request.data = request.DELETE
        else:
            request.data = ast.literal_eval(request.body)


def authenticate(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        init_rest(request)
        if 'key' not in request.data.keys() or 'secret' not in request.data.keys():
            return errno.response_with_erron(errno.ERROR_MISSING_PARAMETER)
        key = request.data['key']
        auth = AuthKey.objects.get(key=key)
        if auth is None:
            return errno.response_with_erron(errno.ERROR_AUTHENTICATE)
        secret_key = auth.secret
        secret_md5 = get_dict_md5(request.data, secret_key)
        if secret_md5 != request.data['secret']:
            return errno.response_with_erron(errno.ERROR_AUTHENTICATE)
        return view(request, *args, **kwargs)
    return wrapper


def request_filter(accept):
    def wrapper(view):
        @wraps(view)
        def view_wrapper(request, *args, **kwargs):
            if request.method not in accept:
                return errno.response_invalid_request_method()
            return view(request, *args, **kwargs)
        return view_wrapper
    return wrapper


def request_parameter(keys):
    def wrapper(view):
        @wraps(view)
        def view_wrapper(request, *args, **kwargs):
            init_rest(request)
            for key in keys:
                if key not in request.data.keys():
                    return errno.response_missing_parameter()
            return view(request, *args, **kwargs)
        return view_wrapper
    return wrapper