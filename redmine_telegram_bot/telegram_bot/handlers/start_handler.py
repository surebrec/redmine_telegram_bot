import os
import sys

import django
from telegram import Update
from telegram.ext import CallbackContext

from telegram_bot.models import Chat

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'redmine_telegram_bot.settings')
django.setup()


def command_start(update: Update, context: CallbackContext) -> None:
    template_text = 'Привет, {first_name}.'
    text = template_text.format(
        first_name=update.effective_user.username,
        chat_id=update.effective_chat.id,
    )
    chat, created = Chat.objects.get_or_create(
        name='default',
        chat_id=update.effective_chat.id,
        is_active=True)
    if not created:
        if not chat.is_active:
            chat.is_active = True
            chat.save()
        text = 'Бот уже работает)'
    update.message.reply_text(text=text)


def command_stop(update: Update, context: CallbackContext) -> None:
    try:
        chat = Chat.objects.get(chat_id=update.effective_chat.id)
        chat.is_active = False
        chat.save()
        text = 'Бот остановлен...'
    except Chat.DoesNotExist:
        text = 'Бот уже остановлен('
    finally:
        update.message.reply_text(text=text)
