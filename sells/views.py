import json
from django.http import HttpResponse
from filters.filter import request_filter, request_parameter, request_login
from images.image_set import create_image_set
from models import PostSell


@request_filter(['POST'])
@request_parameter(['username', 'images', 'description'])
@request_login
def view_new_post(request):
    new_post = PostSell.objects.create()
    new_post.user = request.user
    new_post.image_set = create_image_set(request.data['images'].split(','))
    new_post.description = request.data['description']
    new_post.save()
    return HttpResponse(json.dumps({'success': True, 'id': new_post.id}))