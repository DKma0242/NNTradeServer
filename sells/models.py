from django.db import models
from django.contrib.auth.models import User
from images.models import ImageSet


class PostSell(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField(default='')
    description = models.TextField(default='')
    image_set = models.ForeignKey(ImageSet)
    is_open = models.BooleanField(default=True)
    post_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
