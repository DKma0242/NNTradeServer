from django.http import HttpResponse
from wrappers.filter import request_filter, request_parameter, request_login


@request_filter(['POST', 'GET'])
def view_image(request):
    if request.method == 'POST':
        return HttpResponse("Pass")
    if request.method == 'GET':
        return HttpResponse("Pass")


@request_filter(['POST', 'GET'])
def view_thumbnail(request):
    if request.method == 'POST':
        return HttpResponse("Pass")
    if request.method == 'GET':
        return HttpResponse("Pass")


@request_filter(['POST', 'GET', 'PUT'])
def view_image_set(request):
    if request.method == 'POST':
        return HttpResponse("Pass")
    if request.method == 'GET':
        return HttpResponse("Pass")