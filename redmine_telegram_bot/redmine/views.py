import json

from django.http import JsonResponse
from django.views import View
from django.conf import settings
from telegram import Update

from redmine_telegram_bot.celery import app

from telegram_bot.dispatcher import dispatcher
from telegram_bot.main import telegram_bot


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, telegram_bot)
    dispatcher.process_update(update)


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        if settings.DEBUG:
            process_telegram_event(json.loads(request.body))
        else:
            process_telegram_event.delay(json.loads(request.body))
        return JsonResponse({"ok": "POST received"})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "chilling"})
