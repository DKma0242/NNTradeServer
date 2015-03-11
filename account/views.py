import json
import hashlib
from datetime import datetime
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from auth.auth import authenticate
from erron import errno
from models import UserToken


@authenticate
def view_user(request):
    if request.method == 'POST':
        return register(request)
    return errno.response_invalid_request_method()


@authenticate
def view_token(request):
    if request.method == 'POST':
        return login(request)
    if request.method == 'DELETE':
        return logout(request)
    return errno.response_invalid_request_method()


def register(request):
    if 'username' not in request.POST:
        return errno.response_missing_parameter()
    if 'password' not in request.POST:
        return errno.response_missing_parameter()
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


def login(request):
    if 'username' not in request.POST:
        return errno.response_missing_parameter()
    if 'password' not in request.POST:
        return errno.response_missing_parameter()
    username = request.POST['username']
    if User.objects.filter(username=username) == 0:
        return errno.response_with_erron(errno.ERRON_USERNAME_NON_EXIST)
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is None:
        return errno.response_with_erron(errno.ERRON_MISMATCH_USERNAME_PASSWORD)
    token = hashlib.md5(username + datetime.now().isoformat(' ')).hexdigest()
    user_token = UserToken(user=user, token=token)
    user_token.save()
    return HttpResponse(json.dumps({'success': True}))


def logout(request):
    if 'token' not in request.DELETE:
        return errno.response_missing_parameter()
    token = request.DELETE['token']
    UserToken.objects.filter(token=token).delete()
    return HttpResponse(json.dumps({'success': True}))