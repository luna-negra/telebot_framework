from functools import partial
from core.routes import (connector_callback,
                         connector_command,
                         connector_message,)
from project.views import *


# Mapping handlers and views for Telegram Bot commands.
# This is a test code
COMMANDS: list = [
    connector_command(view=command_start, set_route="main")
]


MESSAGES: list = [
    connector_message(view=get_message, allowed_route="btn1"),
]


CALLBACKS: list = [
    connector_callback(view=callback_btn1, allowed_route="main", set_route="btn1", callback_data="btn1",),
    connector_callback(view=callback_btn2, allowed_route="main", set_route="btn2", callback_data="btn2",),
    connector_callback(view=callback_other, set_route="main")
]