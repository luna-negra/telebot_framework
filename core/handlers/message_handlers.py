# Deprecated



from telebot.util import quick_markup
from telebot.types import ForceReply
from core.handlers import MessageReceiver
from execute import bot


class MessageReceiverBasic(MessageReceiver):
    def __init__(self, message, **kwargs):
        super(MessageReceiverBasic, self).__init__(message=message)
        self.bot_text: str | None = kwargs.get("bot_text", None)
        self.bot_markup = kwargs.get("bot_markup", None)

    async def send_message(self) -> None:
        await bot.send_message(chat_id=self.chat_id,
                               text=self.bot_text,
                               reply_markup=self.bot_markup)
        return None


class MessageReceiverWithForceReply(MessageReceiverBasic):
    def __init__(self, message, **kwargs):
        super(MessageReceiverWithForceReply, self).__init__(message=message, **kwargs)
        self.bot_markup = ForceReply()


class MessageReceiverWithInlineMarkup(MessageReceiverBasic):
    def __init__(self, message, **kwargs):
        super(MessageReceiverWithInlineMarkup, self).__init__(message=message, **kwargs)
        self.bot_markup = quick_markup(values=kwargs.get("inline_json", {}), row_width=kwargs.get("row_with", 2))
