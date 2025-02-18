from telebot.types import ForceReply
from telebot.util import quick_markup
from core.handlers import *
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
    class Meta:
        fields = None
        reply_text = None

    def __init__(self, types, **kwargs):
        super(ReceiverWithForceReply, self).__init__(types=types, **kwargs)
        self.client_data = CLIENT_INFO[self.chat_id]["data"]
        self.bot_markup = ForceReply()
        self.fields = self.Meta.fields
        self.reply_text = self.Meta.reply_text if self.Meta.reply_text is not None else {field:field for field in self.fields}

    async def get_input(self) -> bool:
        flag: bool = False
        index: int = CLIENT_INFO[self.chat_id].get("index")

        if index < len(self.fields):
            if index != 0:
                self.client_data.update({self.fields[index - 1]: self.client_response})

            field = self.fields[index]
            self.bot_text = self.reply_text[field]

            await super().send_message()
            CLIENT_INFO[self.chat_id].update({"index": index + 1})

        else:
            self.client_data.update({self.fields[index - 1]: self.client_response})
            CLIENT_INFO[self.chat_id].update({"index": 0})
            await self.process_input()
            flag = True

        return flag

    async def process_input(self) -> bool:
        pass




class ReceiverWithInlineMarkup(ReceiverBasic):
    def __init__(self, types, **kwargs):
        super(ReceiverWithInlineMarkup, self).__init__(types=types, **kwargs)
        self.bot_markup = quick_markup(values=kwargs.get("inline_json", {}), row_width=kwargs.get("row_width", 2))
