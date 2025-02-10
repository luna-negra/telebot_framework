# Now Testing
from core.routes import route_process, CLIENT_INFO
from core.handlers.callback_handlers import *
from core.handlers.command_handlers import *
from core.handlers.message_handlers import *
from project.serializers import (GetForceReplySerializer,
                                 GetCallbackSerializers, GetMessageSerializer, )


# This is a test code
async def command_start(message):
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


async def callback_btn1(callback):
    inline_json = {
        "btn_a": {"callback_data": "btn_a"},
        "btn_b": {"callback_data": "btn_b"},
        "btn_c": {"callback_data": "btn_c"},
        "btn_d": {"callback_data": "btn_d"},
    }

    #handler_sr = CallbackReceiverWithInlineMarkup(callback=callback,
    #                                             bot_text="you are now in btn1 route",
    #                                             inline_json=inline_json,
    #                                             row_with=2)
    handler_sr = CallbackReceiverWithForceReply(callback=callback,
                                                bot_text="Type any text.",)


    await handler_sr.send_message()


async def callback_btn2(callback):
    handler_sr = GetCallbackSerializers(callback=callback)
    await handler_sr.get_callback()


async def get_message(message):
    handler_sr = GetMessageSerializer(message=message)
    await handler_sr.get_message()



async def callback_other(callback):
    handler_sr = GetCallbackSerializers(callback=callback)
    await handler_sr.get_callback()