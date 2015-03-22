import json
from django.http import HttpResponse
from wrappers.wrapper import request_filter, request_parameter, request_login, allow_empty
from images.image_set import create_image_set, update_image_set
from errnos import errno
from models import PostSell


@request_filter(['POST'])
@request_parameter(['username'])
@request_login
@allow_empty(['title', 'description', 'images'])
def view_new_post(request):
    new_post = PostSell()
    new_post.user = request.user
    new_post.title = request.data['title']
    new_post.description = request.data['description']
    image_id_list = []
    if request.data['images'] != '':
        image_id_list = request.data['images'].split(',')
    new_post.image_set = create_image_set(image_id_list)
    new_post.save()
    return HttpResponse(json.dumps({'success': True, 'id': new_post.id}))


@request_filter(['PUT'])
@request_parameter(['username'])
@request_login
@allow_empty(['title', 'description', 'images'])
def view_update_post(request, post_sell_id):
    post = PostSell.objects.filter(id=int(post_sell_id))
    if post.count() != 1:
        return errno.response_with_erron(errno.ERRNO_NOT_EXIST)
    post = post[0]
    if post.user.id != request.user.id:
        return errno.response_with_erron(errno.ERRNO_NOT_OWNER)
    post.title = request.data['title']
    post.description = request.data['description']
    image_id_list = []
    if request.data['images'] != '':
        image_id_list = request.data['images'].split(',')
    update_image_set(post.image_set.id, image_id_list)
    post.save()
    return HttpResponse(json.dumps({'success': True}))
