import json
import hashlib
from datetime import datetime
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from filters.filter import request_filter, request_parameter, request_login
from errnos import errno
from models import UserToken


@request_filter(['POST', 'DELETE'])
def view_user(request):
    if request.method == 'POST':
        return register(request)
    if request.method == 'DELETE':
        return delete(request)


@request_filter(['POST', 'DELETE'])
def view_token(request):
    if request.method == 'POST':
        return login(request)
    if request.method == 'DELETE':
        return logout(request)


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
    return HttpResponse(json.dumps({'success': True}))


@request_parameter(['username', 'password'])
def delete(request):
    username = request.data['username']
    if User.objects.filter(username=username).count() == 0:
        return errno.response_with_erron(errno.ERRNO_USERNAME_NON_EXIST)
    password = request.data['password']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return errno.response_with_erron(errno.ERRNO_MISMATCH_USERNAME_PASSWORD)
    user.delete()
    return HttpResponse(json.dumps({'success': True}))


@request_parameter(['username', 'password'])
def login(request):
    username = request.data['username']
    if User.objects.filter(username=username).count() == 0:
        return errno.response_with_erron(errno.ERRNO_USERNAME_NON_EXIST)
    password = request.data['password']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return errno.response_with_erron(errno.ERRNO_MISMATCH_USERNAME_PASSWORD)
    token = hashlib.md5(username + datetime.now().isoformat(' ')).hexdigest()
    user_token = UserToken(user=user)
    user_token.token = token
    user_token.save()
    return HttpResponse(json.dumps({'success': True, 'token': token}))


@request_parameter(['username'])
@request_login
def logout(request):
    token = request.data['token']
    UserToken.objects.filter(token=token).delete()
    return HttpResponse(json.dumps({'success': True}))