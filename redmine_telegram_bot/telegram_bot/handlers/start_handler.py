import os
import django
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'redmine_telegram_bot.settings')
django.setup()


def command_start(update: Update, context: CallbackContext) -> None:
    template_text = 'Привет, {first_name}\.'
    text = template_text.format(
        first_name=update.effective_user.username,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    update.message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN_V2)
