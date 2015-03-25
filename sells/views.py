import json
from django.http import HttpResponse
from django.utils.http import urlunquote
from wrappers.wrapper import request_filter, request_login, allow_empty
from images.image_set import create_image_set, update_image_set
from errnos import errno
from models import PostSell


@request_filter(['POST'])
@request_login
@allow_empty(['title', 'description', 'image_id_list'])
def view_new_post(request):
    new_post = PostSell()
    new_post.user = request.user
    new_post.title = urlunquote(request.data['title'])
    new_post.description = urlunquote(request.data['description'])
    image_id_list = []
    if request.data['image_id_list'] != '':
        image_id_list = urlunquote(request.data['image_id_list']).split(',')
    new_post.image_set = create_image_set(image_id_list)
    new_post.save()
    return HttpResponse(json.dumps({'success': True, 'post_id': new_post.id}))


@request_filter(['GET', 'PUT', 'DELETE'])
def view_post(request, post_sell_id):
    if request.method == 'GET':
        return view_get_post(post_sell_id)
    if request.method == 'PUT':
        return view_update_post(request, post_sell_id)
    if request.method == 'DELETE':
        return view_delete_post(request, post_sell_id)


def format_post_data(post):
    return {
        'post_id': post.id,
        'title': post.title,
        'description': post.description,
        'user_id': post.user.id,
        'image_set_id': post.image_set.id,
        'post_date': post.post_date.strftime("%Y-%m-%d %H:%M:%S"),
        'modify_date': post.modify_date.strftime("%Y-%m-%d %H:%M:%S"),
        'is_open': post.is_open,
    }


def view_get_post(post_sell_id):
    post = PostSell.objects.filter(id=int(post_sell_id))
    if post.count() != 1:
        return errno.response_with_erron(errno.ERRNO_NOT_EXIST)
    post = post[0]
    data = {
        'success': True,
        'post': format_post_data(post)
    }
    return HttpResponse(json.dumps(data))


@request_login
def view_update_post(request, post_sell_id):
    post = PostSell.objects.filter(id=int(post_sell_id))
    if post.count() != 1:
        return errno.response_with_erron(errno.ERRNO_NOT_EXIST)
    post = post[0]
    if post.user.id != request.user.id:
        return errno.response_with_erron(errno.ERRNO_NOT_OWNER)
    if 'title' in request.data.keys():
        post.title = urlunquote(request.data['title'])
    if 'description' in request.data.keys():
        post.description = urlunquote(request.data['description'])
    if 'is_open' in request.data.keys():
        post.is_open = request.data['is_open'] == 'true'
    if 'image_id_list' in request.data.keys():
        image_id_list = []
        if request.data['image_id_list'] != '':
            image_id_list = urlunquote(request.data['image_id_list']).split(',')
        update_image_set(post.image_set.id, image_id_list)
    post.save()
    return HttpResponse(json.dumps({'success': True}))


@request_login
def view_delete_post(request, post_sell_id):
    post = PostSell.objects.filter(id=int(post_sell_id))
    if post.count() != 1:
        return errno.response_with_erron(errno.ERRNO_NOT_EXIST)
    post = post[0]
    if post.user.id != request.user.id:
        return errno.response_with_erron(errno.ERRNO_NOT_OWNER)
    post.delete()
    return HttpResponse(json.dumps({'success': True}))


@request_filter(['GET'])
def view_posts(request, page_num):
    page_num = int(page_num)
    if page_num == 0:
        page_num = 1
    posts = PostSell.objects.order_by('-post_date')[(page_num - 1) * 20:page_num * 20 - 1]
    data = {
        'success': True,
        'posts': [format_post_data(post) for post in posts],
    }
    return HttpResponse(json.dumps(data))
