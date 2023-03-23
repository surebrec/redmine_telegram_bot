from telegram import Update

from redmine_telegram_bot.celery import app

from telegram_bot.dispatcher import dispatcher
from telegram_bot.main import telegram_bot
from telegram_bot.models import Chat


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, telegram_bot)
    dispatcher.process_update(update)


@app.task(ignore_result=True)
def send_scheduled_hello():
    chats = Chat.objects.filter(is_active=True)
    message = 'It is a scheduled message!'
    for chat in chats:
        send_message.delay(chat.chat_id, message)


@app.task(ignore_result=True)
def send_message(chat_id, message):
    telegram_bot.send_message(chat_id=chat_id, text=message)
