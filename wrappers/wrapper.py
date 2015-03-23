import ast
import hashlib
import operator
from collections import OrderedDict
from functools import wraps
from django.contrib.auth.models import User
from errnos import errno
from account.models import UserToken


def get_dict_md5(data, token):
    sorted_data = data.copy()
    sorted_data['token'] = token
    sorted_data = OrderedDict(sorted(sorted_data.items(), key=operator.itemgetter(0)))
    text = '&'.join([key + '=' + value for key, value in sorted_data.items()])
    return hashlib.md5(text).hexdigest()


def init_rest(request):
    if not hasattr(request, 'data'):
        if request.method == 'GET':
            request.data = request.GET.copy()
        elif request.method == 'POST':
            request.data = request.POST.copy()
        elif request.method == 'PUT':
            request.PUT = ast.literal_eval(request.body)
            request.data = request.PUT
        elif request.method == 'DELETE':
            request.DELETE = ast.literal_eval(request.body)
            request.data = request.DELETE
        else:
            request.data = ast.literal_eval(request.body)


def request_login(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        init_rest(request)
        if 'user_id' not in request.data.keys() or 'token' not in request.data.keys():
            return errno.response_with_erron(errno.ERRNO_MISSING_PARAMETER)
        user_id = request.data['user_id']
        user = User.objects.filter(id=user_id)
        if user.count() == 0:
            return errno.response_with_erron(errno.ERRNO_USERNAME_NON_EXIST)
        user = user[0]
        user_token = UserToken.objects.filter(user=user)
        if user_token.count() == 0:
            return errno.response_with_erron(errno.ERRNO_NO_TOKEN)
        real_token = user_token[0].token
        encrypt_token = get_dict_md5(request.data, real_token)
        sent_token = request.data['token']
        if sent_token != encrypt_token:
            return errno.response_with_erron(errno.ERRNO_MISMATCH_TOKEN)
        request.user = user
        return view(request, *args, **kwargs)
    return wrapper


def request_filter(accept):
    def wrapper(view):
        @wraps(view)
        def view_wrapper(request, *args, **kwargs):
            if request.method not in accept:
                return errno.response_with_erron(errno.ERRNO_INVALID_REQUEST_METHOD)
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
                    return errno.response_with_erron(errno.ERRNO_MISSING_PARAMETER)
            return view(request, *args, **kwargs)
        return view_wrapper
    return wrapper


def allow_empty(keys):
    def wrapper(view):
        @wraps(view)
        def view_wrapper(request, *args, **kwargs):
            init_rest(request)
            for key in keys:
                if key not in request.data.keys():
                    request.data[key] = ''
            return view(request, *args, **kwargs)
        return view_wrapper
    return wrapper