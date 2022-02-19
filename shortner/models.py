from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User


class UrlList(models.Model):
    key = models.CharField(max_length=20)
    url = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=CASCADE)
    date_added = models.DateField(auto_now_add=True)
    total_clicks = models.IntegerField(default=0)


class Clicks(models.Model):
    key_id = models.ForeignKey(UrlList, on_delete=CASCADE)
    date_added = models.DateField(auto_now_add=True)
