from telebot.types import ForceReply
from telebot.util import quick_markup
from core.handlers import Receiver
from core.routes import CLIENT_INFO
from execute import bot


class ReceiverBasic(Receiver):
    def __init__(self, types, **kwargs):
        super(ReceiverBasic, self).__init__(types=types)
        self.bot_text: str | None = kwargs.get("bot_text", None)
        self.bot_markup = kwargs.get("bot_markup", None)
        self.route = kwargs.get("route", None)
        if self.route is not None:
            CLIENT_INFO[self.chat_id].update({"route": self.route})

    async def send_message(self) -> None:
        await bot.send_message(chat_id=self.chat_id,
                               text=self.bot_text,
                               reply_markup=self.bot_markup)
        return None


class ReceiverWithForceReply(ReceiverBasic):
    def __init__(self, types, **kwargs):
        super(ReceiverWithForceReply, self).__init__(types=types, **kwargs)
        self.bot_markup = ForceReply()


class ReceiverWithInlineMarkup(ReceiverBasic):
    def __init__(self, types, **kwargs):
        super(ReceiverWithInlineMarkup, self).__init__(types=types, **kwargs)
        self.bot_markup = quick_markup(values=kwargs.get("inline_json", {}), row_width=kwargs.get("row_width", 2))
