from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models


# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)


class App(models.Model):
    class Meta:
        unique_together = (('user', 'app_name'),)
    user = models.ForeignKey(User)
    app_name = models.CharField(max_length=100)