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


def command_start(update: Update, context: CallbackContext) -> None:
    logger.info('Start command activated')
    chat, created = Chat.objects.get_or_create(
        chat_id=update.effective_chat.id)
    if created or not chat.is_active:
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
