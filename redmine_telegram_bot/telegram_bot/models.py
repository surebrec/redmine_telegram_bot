from django.db import models


class Bot(models.Model):
    token = models.CharField(max_length=256)


class Chat(models.Model):
    name = models.CharField(max_length=150)
    chat_id = models.IntegerField()
    is_active = models.BooleanField(default=False)
