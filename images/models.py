from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    user = models.ForeignKey(User)


class ImageSet(models.Model):
    pass


class ImageImageSet(models.Model):
    image_set = models.ForeignKey(ImageSet)
    image = models.ForeignKey(Image)