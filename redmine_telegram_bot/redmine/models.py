from django.contrib import admin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class RedmineGroup(models.Model):
    name = models.CharField(max_length=150, default='Redmine Group')
    group_id = models.IntegerField(verbose_name='ID группы Redmine',
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(5000)],
                                   unique=True)
    is_valid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Группа Redmine'
        verbose_name_plural = 'Группы Redmine'

    def __str__(self):
        return f'{self.name}'


class RedmineUser(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=250)
    user_id = models.IntegerField(verbose_name='ID пользователя Redmine',
                                  validators=[MinValueValidator(0), ])
    group = models.ForeignKey(
        RedmineGroup,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Группа Redmine',
    )

    @admin.display(description='Пользователь')
    def short_name(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Пользователь Redmine'
        verbose_name_plural = 'Пользователи Redmine'
        ordering = ('id',)

    def __str__(self):
        try:
            return '{} {:1.1}.{:1.1}.'.format(*self.name.split())
        except IndexError:
            return self.name
