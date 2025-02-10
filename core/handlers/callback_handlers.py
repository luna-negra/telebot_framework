from telebot.util import quick_markup
from telebot.types import ForceReply
from core.handlers import CallbackReceiver
from main import bot


class CallbackReceiverBasic(CallbackReceiver):
    """
    CallbackReceiverBasic
    this class is charge of receiving callback data from client.

    """

    def __init__(self, callback=None, **kwargs):
        super(CallbackReceiverBasic, self).__init__(callback=callback)
        self.bot_text: str = kwargs.get("bot_text")
        self.bot_markup = kwargs.get("bot_markup", None)

    async def send_message(self) -> None:
        await bot.send_message(chat_id=self.chat_id,
                               text=self.bot_text,
                               reply_markup=self.bot_markup)
        return None


class CallbackReceiverWithForceReply(CallbackReceiverBasic):
    """
    CallbackReceiverWithForceReply
    this class is charge of receiving callback data from client and return ForceReply markup.

    """

    def __init__(self, callback=None, **kwargs):
        super(CallbackReceiverWithForceReply, self).__init__(callback=callback, **kwargs)
        self.bot_markup = ForceReply()


class CallbackReceiverWithInlineMarkup(CallbackReceiverWithForceReply):
    """
    CallbackReceiverWithInlineMarkup:
    this class is charge of receiving callback data from client and return quick_markup markup.

    """

    def __init__(self, callback=None, **kwargs):
        super(CallbackReceiverWithInlineMarkup, self).__init__(callback=callback)
        self.bot_markup = quick_markup(values=kwargs.get("inline_json"), row_width=kwargs.get("row_with", 2))
