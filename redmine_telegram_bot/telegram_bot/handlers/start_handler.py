import logging
import os

import django
from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.models import Chat

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'redmine_telegram_bot.settings')
django.setup()

logger = logging.getLogger(__name__)


def get_chat_name(update: Update):
    if update.effective_chat.type == 'private':
        return (f'{update.effective_chat.first_name} '
                f'{update.effective_chat.last_name}')
    return update.effective_chat.title


def command_start(update: Update, context: CallbackContext) -> None:
    logger.info('Start command activated')
    chat, created = Chat.objects.get_or_create(
        chat_id=update.effective_chat.id)
    if created or not chat.is_active:
        chat.name = get_chat_name(update)
        chat.is_active = True
        chat.save()
        text = 'Бот начинает свою работу'
    else:
        text = 'Бот уже работает'

    update.effective_chat.send_message(text=text)


def command_stop(update: Update, context: CallbackContext) -> None:
    logger.info('Stop command activated')
    try:
        chat = Chat.objects.get(chat_id=update.effective_chat.id)
        chat.is_active = False
        chat.save()
        text = 'Бот остановлен...'
    except Chat.DoesNotExist:
        text = 'Бот уже остановлен('
    update.effective_chat.send_message(text=text)
