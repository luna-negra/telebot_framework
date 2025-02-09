# Now Testing
from core.routes import route_process
from core.handlers.command_handlers import *
from core.handlers.message_handlers import *
from project.serializers import (GetForceReplySerializer,
                                 GetCallbackSerializers,)


# This is a test code
async def command_start(message, **kwargs):
    route_process(message=message, **kwargs)
    inline_json = {
        "btn1": {"callback_data": "btn1"},
        "btn2": {"callback_data": "btn2"},
        "btn3": {"callback_data": "btn3"},
        "btn4": {"callback_data": "btn4"},
    }

    handler_sr = CommandReceiverWithInlineMarkup(message=message,
                                                 bot_text="Welcome. Please Select one of Buttons",
                                                 inline_json=inline_json,
                                                 row_with=3)
    await handler_sr.send_message()


async def callback_start(callback, **kwargs):
    route_process(callback=callback, **kwargs)
    handler_sr = GetCallbackSerializers(callback=callback)

    await handler_sr.get_callback()
