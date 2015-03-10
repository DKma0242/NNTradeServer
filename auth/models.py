from django.db import models


class AuthKey(models.Model):
    key = models.CharField(max_length=64, db_index=True)
    secret = models.CharField(max_length=64)