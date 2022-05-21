from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mob_number = models.IntegerField(default=0)
    address = models.CharField(max_length=500, default="")
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user_name