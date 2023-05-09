from telegram import Update
from redmine_telegram_bot.celery import app
from telegram_bot.dispatcher import dispatcher
from telegram_bot.main import telegram_bot


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, telegram_bot)
    dispatcher.process_update(update)
