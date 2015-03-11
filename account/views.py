import json
import hashlib
from datetime import datetime
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from auth.auth import authenticate, request_filter, request_parameter
from erron import errno
from models import UserToken


@request_filter(['POST'])
@authenticate
def view_user(request):
    if request.method == 'POST':
        return register(request)


@request_filter(['POST', 'DELETE'])
@authenticate
def view_token(request):
    if request.method == 'POST':
        return login(request)
    if request.method == 'DELETE':
        return logout(request)


@request_parameter(['username', 'password'])
def register(request):
    username = request.POST['username']
    if User.objects.filter(username=username).count() > 0:
        return errno.response_with_erron(errno.ERRON_USERNAME_EXIST)
    password = request.POST['password']
    user = User.objects.create_user(username=username,
                                    password=password,
                                    email='')
    user.first_name = username
    user.save()
    return HttpResponse(json.dumps({'success': True}))


@request_parameter(['username', 'password'])
def login(request):
    username = request.POST['username']
    if User.objects.filter(username=username).count() == 0:
        return errno.response_with_erron(errno.ERRON_USERNAME_NON_EXIST)
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return errno.response_with_erron(errno.ERRON_MISMATCH_USERNAME_PASSWORD)
    token = hashlib.md5(username + datetime.now().isoformat(' ')).hexdigest()
    user_token = UserToken(user=user, token=token)
    user_token.save()
    return HttpResponse(json.dumps({'success': True, 'token': token}))


@request_parameter(['username', 'token'])
def logout(request):
    token = request.DELETE['token']
    UserToken.objects.filter(token=token).delete()
    return HttpResponse(json.dumps({'success': True}))