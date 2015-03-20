import json
from django.http import HttpResponse
from wrappers.filter import request_filter, request_parameter, request_login, allow_empty
from images.image_set import create_image_set
from models import PostSell


@request_filter(['POST'])
@request_parameter(['username'])
@request_login
@allow_empty(['images', 'description'])
def view_new_post(request):
    new_post = PostSell()
    new_post.user = request.user
    image_id_list = ''
    if request.data['images'] != '':
        image_id_list = request.data['images'].split(',')
    new_post.image_set = create_image_set(image_id_list)
    new_post.description = request.data['description']
    new_post.save()
    return HttpResponse(json.dumps({'success': True, 'id': new_post.id}))