from functools import partial
from core.routes import (command_connector,
                         message_connector,
                         callback_connector)
from project.views import *


# Mapping handlers and views for Telegram Bot commands.
# This is a test code
COMMANDS: list = [
    command_connector(view=command_start, set_route="main")
]


MESSAGES: list = [
    message_connector(view=get_message, allowed_route="btn1"),
]


CALLBACKS: list = [
    callback_connector(view=callback_btn1, func=lambda callback: callback.data == "btn1", allowed_route="main", set_route="btn1"),
    callback_connector(view=callback_other, allowed_route="main")
]