from core.routes import (connector_callback,
                         connector_command,
                         connector_message,)
from project.views import *


# Mapping handlers and views for Telegram Bot commands.
COMMANDS: list = [
    connector_command(view=main, set_route="main"),
]


MESSAGES: list = [
    connector_message(view=signin_prompt, allowed_route="signin"),
]


CALLBACKS: list = [
    connector_callback(view=signin, set_route="signin", allowed_route="main"),
    connector_callback(view=signup, set_route="signup", allowed_route="main"),
]
