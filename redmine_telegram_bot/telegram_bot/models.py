import logging
from django.db import models
from django_celery_beat.models import PeriodicTask

from redmine.models import RedmineGroup

logger = logging.getLogger(__name__)


class Chat(models.Model):
    name = models.CharField(max_length=150, default='Default Chat')
    chat_id = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(RedmineGroup,
                                    related_name='groups_chats',
                                    through='ChatRedmineGroup')
    tasks = models.ManyToManyField(PeriodicTask,
                                   related_name='tasks',
                                   through='ChatTask', blank=False)


class ChatRedmineGroup(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    groups = models.ForeignKey(RedmineGroup, on_delete=models.CASCADE)


class ChatTask(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)
