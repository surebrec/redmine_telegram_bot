from django.db import models
from django.core.validators import MinValueValidator


class Widget(models.Model):
    name = models.CharField(default='Widget name', max_length=100)


class RedmineUser(models.Model):
    redmine_id = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

