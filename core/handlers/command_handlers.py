from telebot.util import quick_markup
from telebot.types import ForceReply
from core.handlers import MsgReceiver
from execute import bot


class CommandReceiver(MsgReceiver):
    """
    CommandReceiver:
    this class is charge of receiving command from client

    """

    def __init__(self, message, **kwargs):
        super(CommandReceiver, self).__init__(message=message)
        self.command: str = message.text.replace("/", "")
        self.entities = message.entities
        self.bot_text: str | None = kwargs.get("bot_text", None)
        self.bot_markup = kwargs.get("bot_markup", None)


    async def send_message(self) -> None:
        await bot.send_message(chat_id=self.chat_id,
                               text=self.bot_text,
                               reply_markup=self.bot_markup)
        return None


class CommandReceiverWithForceReply(CommandReceiver):
    """
    CommandReceiverWithForceReply:
    this class is charge of receiving command from client and return ForceReply markup.

    """

    def __init__(self, message, **kwargs):
        super(CommandReceiverWithForceReply, self).__init__(message=message, **kwargs)
        self.bot_markup = ForceReply()


class CommandReceiverWithInlineMarkup(CommandReceiver):
    """
    CommandReceiverWithInlineMarkup:
    this class is charge of receiving command from client and return quick_markup markup.

    """

    def __init__(self, message=None, **kwargs):
        super(CommandReceiverWithInlineMarkup, self).__init__(message=message, **kwargs)
        self.bot_markup = quick_markup(values=kwargs.get("inline_json", {}), row_width=kwargs.get("row_with", 2))
