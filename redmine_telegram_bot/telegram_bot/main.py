import logging
import sys

import telegram
from telegram import Bot
from django.conf import settings


def create_bot():
    try:
        bot = Bot(settings.TELEGRAM_TOKEN)
        telegram_bot_username = bot.get_me()['username']
    except telegram.error.Unauthorized:
        logging.error('Telegram token is invalid')
        sys.exit(1)
    else:
        logging.info(f'Bot {telegram_bot_username} started.')
        return bot


telegram_bot = create_bot()
