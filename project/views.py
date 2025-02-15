from core.handlers.callback_handlers import *
from core.handlers.command_handlers import *
from core.handlers.message_handlers import *
from project.serializers import *


# please write down your code below.
# Main
async def main(message) -> None:
    handler_sr = Main(message=message,)
    await handler_sr.send_message()
    return None


# Sign In: callback response
async def signin(callback) -> None:
    handler_sr = Signin(callback=callback, bot_text="[Sign In]\nInput Username")
    await handler_sr.send_message()
    return None


# Sign In: prompt response
async def signin_prompt(message) -> None:
    handler_sr = SignInPrompt(message=message, bot_text="[Sign In]\nInput Password")
    await handler_sr.get_message()
    await handler_sr.send_message()
    return None


# Sign Up
async def signup(callback) -> None:
    handler_sr = None
    return None