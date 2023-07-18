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
    effective_chat = update.effective_chat
    router = {
        'private': lambda chat: f'{chat.first_name} {chat.last_name}',
        'group': lambda chat: chat.title,
        'default': lambda chat: f'default chat ({chat.chat_id})',
    }
    return router.get(effective_chat.type, 'default')(effective_chat)


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
