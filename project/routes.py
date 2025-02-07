from core.routes import (command_connector,
                         message_connector,
                         callback_connector,)
from project.views import *


# Mapping handlers and views for Telegram Bot commands.
# This is a test code
COMMANDS: list = [
    command_connector(view=command_general, commands=["start", "main"]),
    command_connector(view=command_force_reply, commands=["test1"]),
    command_connector(view=command_inline_markup, commands=["test2"]),
]


MESSAGES: list = [
    message_connector(view=get_force_reply, func=lambda message: True)
]


CALLBACKS: list = [
    callback_connector(view=get_callback, func=lambda callback: True)
]