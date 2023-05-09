from telegram.ext import Dispatcher, CommandHandler, Filters
from .handlers.start_handler import command_start, command_stop
from .handlers.redmine_handlers import command_update, command_time_entries
from django.conf import settings
from .main import telegram_bot


def setup_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler('start', command_start))
    dp.add_handler(CommandHandler('stop', command_stop))
    dp.add_handler(CommandHandler('update', command_update,
                                  Filters.user(username='@Michael_Kasat')))
    dp.add_handler(CommandHandler('time_entries', command_time_entries,
                                  Filters.user(username='@Michael_Kasat')))

    return dp


n_workers = 0 if settings.DEBUG else 4
dispatcher = setup_dispatcher(
    Dispatcher(bot=telegram_bot,
               workers=n_workers,
               use_context=True,
               update_queue=None)
)
