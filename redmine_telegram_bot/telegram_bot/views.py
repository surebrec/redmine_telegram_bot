import json
from .tasks import process_telegram_event
from django.http import JsonResponse
from django.views import View
from django.conf import settings


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        if settings.DEBUG:
            process_telegram_event(json.loads(request.body))
        else:
            process_telegram_event.delay(json.loads(request.body))
        return JsonResponse({"ok": "POST received"})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "chilling"})
