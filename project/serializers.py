# please import handlers classes in core.handlers
# and inherit one of them to your custom handler serializer classes.
# from core.handlers.command_handlers import *
# from core.handlers.message_handlers import *
# from main import bot


# This is a Test Code

from core.handlers.message_handlers import *
from core.handlers import CallbackReceiver
from main import bot


class GetForceReplySerializer(MessageForceReply):
    async def get_message(self, message) -> None:
        if self.client_text == "password":
            text = "Password matched. Welcome"

        else:
            text = "Password is not Match"

        await bot.send_message(chat_id=message.from_user.id,
                               text=text)
        return None


class GetCallbackSerializers(CallbackReceiver):
    async def get_callback(self):
        await bot.send_message(chat_id=self.chat_id,
                               text=f"you clicked {self.callback_data}")
