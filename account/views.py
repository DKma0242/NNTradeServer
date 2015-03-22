import json
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from wrappers.wrapper import request_filter, request_parameter
from errnos import errno
from models import UserToken


@request_filter(['POST'])
@request_parameter(['username', 'password'])
def register(request):
    username = request.data['username']
    if User.objects.filter(username=username).count() > 0:
        return errno.response_with_erron(errno.ERRNO_USERNAME_EXIST)
    password = request.data['password']
    user = User.objects.create_user(username=username,
                                    password=password,
                                    email='')
    user.first_name = username
    user.save()
    UserToken.objects.create(user=user, token=password)
    return HttpResponse(json.dumps({'success': True, 'user_id': user.id}))


@request_filter(['POST'])
@request_parameter(['username', 'password'])
def login(request):
    username = request.data['username']
    if User.objects.filter(username=username).count() == 0:
        return errno.response_with_erron(errno.ERRNO_USERNAME_NON_EXIST)
    password = request.data['password']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return errno.response_with_erron(errno.ERRNO_MISMATCH_USERNAME_PASSWORD)
    return HttpResponse(json.dumps({'success': True, 'user_id': user.id}))
