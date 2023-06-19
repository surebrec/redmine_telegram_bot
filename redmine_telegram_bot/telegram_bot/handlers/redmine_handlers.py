import os

import django
from telegram import Update
from telegram.ext import CallbackContext
from redmine.tasks import update_redmine_groups_data, send_time_entries
from telegram_bot.models import Chat
from telegram_bot.exceptions import ChatException

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'redmine_telegram_bot.settings')
django.setup()


def check_chat(update):
    chat_id = update.effective_chat.id
    try:
        chat = Chat.objects.get(chat_id=chat_id)
    except Chat.DoesNotExist:
        raise ChatException('Бот остановлен, нажмите /start')
    except Exception as ex:
        raise ChatException(f'Ошибка:{ex}')
    if not chat.groups.exists():
        raise ChatException('Чат не привязан к Redmine')
    if not chat.is_active:
        raise ChatException('Бот остановлен, нажмите /start')
    return chat_id


def command_update(update: Update, context: CallbackContext, ) -> None:
    try:
        chat_id = check_chat(update)
    except ChatException as exc:
        update.effective_chat.send_message(str(exc))
    else:
        update_redmine_groups_data.delay(chat_id=chat_id)
        update.effective_chat.send_message('Данные обновлены')


def command_time_entries(from_delta=0, to_delta=0):
    def wrapped(update: Update, context: CallbackContext):
        try:
            chat_id = check_chat(update)
        except ChatException as exc:
            update.effective_chat.send_message(str(exc))
        else:
            send_time_entries.delay(chat_id, from_delta, to_delta)

    return wrapped
