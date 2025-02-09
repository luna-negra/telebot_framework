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
]


CALLBACKS: list = [
    callback_connector(view=callback_start, allowed_route="main"),
]