from telebot.util import quick_markup
from telebot.types import ForceReply
from core.handlers import MsgReceiver
from execute import bot


class MessageReceiver(MsgReceiver):
    async def get_message(self) -> None:
        return None


class MessageReceiverWithForceReply(MessageReceiver):
    def __init__(self, message, **kwargs):
        super(MessageReceiverWithForceReply, self).__init__(message=message)
        self.bot_text: str | None = kwargs.get("bot_text", None)
        self.bot_markup = ForceReply()


    async def send_message(self) -> None:
        await bot.send_message(chat_id=self.chat_id,
                               text=self.bot_text,
                               reply_markup=self.bot_markup)
        return None


class MessageReceiverWithInlineMarkup(MessageReceiverWithForceReply):
    def __init__(self, message, **kwargs):
        super(MessageReceiverWithInlineMarkup, self).__init__(message=message, **kwargs)
        self.bot_markup = quick_markup(values=kwargs.get("inline_json", {}), row_width=kwargs.get("row_with", 2))
