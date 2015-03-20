from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    user = models.ForeignKey(User)


class ImageSet(models.Model):
    image = models.ForeignKey(models)