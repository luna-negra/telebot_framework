# Now Testing
from core.handlers.command_handlers import *
from core.handlers.message_handlers import *
from project.serializers import (GetForceReplySerializer,
                                 GetCallbackSerializers,)


# This is a test code
async def command_general(message):
    handler_sr = CommandReceiver(message=message,
                                 bot_text="Greeting from Test Bot.")
    await handler_sr.send_message()


async def command_force_reply(message):
    handler_sr = CommandReceiverWithForceReply(message=message,
                                               bot_text="Please reply this message")
    await handler_sr.send_message()


async def command_inline_markup(message):
    inline_button: dict = {
        "btn1": {"callback_data": "btn1"},
        "btn2": {"callback_data": "btn2"},
        "btn3": {"callback_data": "btn3"},
        "btn4": {"callback_data": "btn4"},
        "btn5": {"callback_data": "btn5"},
    }

    handler_sr = CommandReceiverWithInlineMarkup(message=message,
                                                 bot_text="Please select one of buttons below.",
                                                 row_with=3,
                                                 markup_json=inline_button)
    await handler_sr.send_message()


async def get_force_reply(message):
    handler_sr = GetForceReplySerializer(message=message)
    await handler_sr.get_message(message)


async def get_callback(callback):
    handler_sr = GetCallbackSerializers(callback=callback)
    await handler_sr.get_callback(callback)