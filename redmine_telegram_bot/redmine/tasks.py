import logging
from datetime import date, timedelta
from celery import group
from aiohttp import ClientConnectorError
from rest_framework import serializers
from telegram.error import NetworkError, TimedOut

from redmine_telegram_bot.celery import app

from redmine.handlers.render_handlers import render_to_message
from redmine.models import RedmineGroup
from telegram_bot.main import telegram_bot
from .serializers import RedmineGroupSerializer
from .client import RedmineAPIClient

logger = logging.getLogger(__name__)


@app.task(autoretry_for=(NetworkError, TimedOut),
          retry_kwargs={'max_retries': 50},
          default_retry_delay=1)
def send_message(message, chat_id):
    telegram_bot.send_message(chat_id=chat_id,
                              text=message,
                              parse_mode='HTML')


@app.task
def send_messages(message, chats_ids):
    group(send_message.s(message, chat_id) for chat_id in chats_ids)()


@app.task(autoretry_for=(ClientConnectorError,),
          retry_kwargs={'max_retries': 5},
          default_retry_delay=60)
def request_time_entries(params):
    client = RedmineAPIClient()
    return client.get_time_entries_data(params=params)


@app.task(autoretry_for=(ClientConnectorError,),
          retry_kwargs={'max_retries': 5},
          default_retry_delay=60)
def request_groups_data(groups_ids, params):
    client = RedmineAPIClient()
    return client.get_group_data(groups_ids, params=params)


@app.task
def request_error_handler(request, exc, traceback):
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
        request.id, exc, traceback))


@app.task
def update_group_data(data):
    try:
        group_data = data.get('group')
        group_instance = RedmineGroup.objects.get(
            group_id=group_data.get('id'))
        serializer = RedmineGroupSerializer(data=group_data,
                                            instance=group_instance)
        if serializer.is_valid():
            serializer.save(is_valid=True)
    except (serializers.ValidationError,
            RedmineGroup.DoesNotExist,
            KeyError):
        pass


@app.task
def update_groups_data(groups_data):
    group(update_group_data.s(group_data) for group_data in groups_data)()


@app.task
def get_groups_ids(chat_id=None):
    if chat_id:
        groups = RedmineGroup.objects.filter(groups_chats__chat_id=chat_id)
    else:
        groups = RedmineGroup.objects.all()
    return list(groups.values_list('group_id', flat=True))


@app.task
def update_redmine_groups_data(groups_ids: list = None,
                               chat_id: int = None) -> None:
    if groups_ids:
        chain = (request_groups_data.s(groups_ids, {'include': 'users'}))
    else:
        chain = (get_groups_ids.s(chat_id) |
                 request_groups_data.s({'include': 'users'}))
    chain |= update_groups_data.s()
    chain()


@app.task(autoretry_for=(ClientConnectorError,),
          retry_kwargs={'max_retries': 5},
          default_retry_delay=60)
def get_time_entries(users, group_name, from_date, to_date):
    client = RedmineAPIClient()
    users_ids = '|'.join(map(str, [user['user_id'] for user in users]))
    users_names = [user['name'] for user in users]
    data = client.get_time_entries_data(
        params={'user_id': users_ids,
                'from': from_date,
                'to': to_date})

    return render_to_message(data,
                             users_names,
                             group_name,
                             from_date,
                             to_date)


@app.task(bind=True)
def send_time_entries(self, chat_id=None, from_delta=0, to_delta=0):
    from_date = str(date.today() - timedelta(days=from_delta))
    to_date = str(date.today() - timedelta(days=to_delta))

    if chat_id:
        groups = RedmineGroup.objects.filter(
            groups_chats__chat_id=chat_id).prefetch_related('users')
    else:
        task_name = self.request.properties.get('periodic_task_name')
        groups = RedmineGroup.objects.filter(
            groups_chats__tasks__name=task_name).prefetch_related(
            'groups_chats').prefetch_related('users')
    for group in groups:
        users = list(group.users.all().values())
        if chat_id:
            chats_ids = [chat_id]
        else:
            chats = group.groups_chats.all().filter(
                is_active=True,
                tasks__name=task_name)
            chats_ids = list(chats.values_list('chat_id', flat=True))
        if chats_ids:
            get_time_entries.apply_async(
                (users, group.name, from_date, to_date),
                link=send_messages.s(chats_ids))
