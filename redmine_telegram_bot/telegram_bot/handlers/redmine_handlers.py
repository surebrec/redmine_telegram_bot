import os

import django
from telegram import Update
from telegram.ext import CallbackContext
from redmine.tasks import update_redmine_groups_data, send_time_entries
from telegram_bot.models import Chat

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'redmine_telegram_bot.settings')
django.setup()


def check_chat(function):
    def wrapp(update: Update, context: CallbackContext) -> None:
        chat_id = update.effective_chat.id
        try:
            chat = Chat.objects.get(chat_id=chat_id)
            if not chat.groups.all().exists():
                message = 'Чат не привязан к Redmine'
            elif not chat.is_active:
                message = 'Бот остановлен, нажмите /start'
            else:
                function(update, context, chat_id)
        except Chat.DoesNotExist:
            message = 'Бот не запущен, нажмите /start'
        except Exception as ex:
            message = f'Ошибка:{ex}'
        update.effective_chat.send_message(message)

    return wrapp


@check_chat
def command_update(update: Update, context: CallbackContext,
                   chat_id) -> None:
    update_redmine_groups_data.delay(chat_id=chat_id)
    update.effective_chat.send_message('Данные обновлены')


@check_chat
def command_time_entries(update: Update, context: CallbackContext,
                         chat_id) -> None:
    update.effective_chat.send_message('Трудозатраты')
    send_time_entries.delay(chat_id, 1, 1)
