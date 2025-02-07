from main import bot
from core.config import ALLOWED_CHAT_TYPE


def command_connector(view, commands:list, **kwargs):
    bot.message_handler(commands=commands,
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(view)

def message_connector(view, func, **kwargs):
    bot.message_handler(func=func,
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(view)


def callback_connector(view, func, **kwargs):
    bot.callback_query_handler(func=func,
                               **kwargs)(view)