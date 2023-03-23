from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from telegram.ext import Updater

from telegram_bot.dispatcher import setup_dispatcher


class Command(BaseCommand):
    help = 'Starts bot polling'

    def handle(self, *args, **options):
        try:
            updater = Updater(settings.TELEGRAM_TOKEN, use_context=True)
            dp = updater.dispatcher
            dp = setup_dispatcher(dp)
            updater.start_polling()
            updater.idle()
        except Exception as ex:
            raise CommandError(f'Error occurred: {ex}.')
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Bot started to poll.'))
