import re
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
        fields_text = None
        fields_regex = None
        fields_error_msg = None

    def __init__(self, types, **kwargs):
        super(ReceiverWithForceReply, self).__init__(types=types, **kwargs)
        self.client_data = CLIENT_INFO[self.chat_id]["data"]
        self.bot_markup = ForceReply()

        self.fields = getattr(self.Meta, 'fields', ())
        self.fields_text = getattr(self.Meta, 'fields_text', {field: field for field in self.fields})
        self.fields_regex = getattr(self.Meta, 'fields_regex', {field: ".*" for field in self.fields})
        self.fields_error_msg = getattr(self.Meta, 'fields_error_msg', {field: f"'{field}' does not match regex." for field in self.fields})

    async def get_client_data(self) -> bool:
        # Exit if there is no fields
        if len(self.fields) == 0:
            # Logger
            return True

        index: int = CLIENT_INFO[self.chat_id].get("index")
        if index != 0 :
            pre_index = index - 1
            pre_field = self.fields[pre_index]
            regex_list = self.fields_regex.get(pre_field, [".*"])
            error_msg = self.fields_error_msg.get(pre_field, f"'{pre_field}' is not satisfying regex.")

            if not isinstance(regex_list, (list, tuple)):
                regex_list = [regex_list]

            if not isinstance(error_msg, (list, tuple)):
                error_msg = [error_msg]

            for regex in regex_list:
                inner_index = regex_list.index(regex)
                if not re.search(pattern=regex, string=self.client_response):
                    self.bot_text = error_msg[0] if len(error_msg) != len(regex_list) else error_msg[inner_index]
                    self.bot_markup = None
                    CLIENT_INFO[self.chat_id].update({"index": 0, "data": {}})
                    await super().send_message()
                    return True

            CLIENT_INFO[self.chat_id]["data"].update({pre_field: self.client_response})

        if index != len(self.fields):
            field = self.fields[index]
            self.bot_text = self.fields_text[field]
            CLIENT_INFO[self.chat_id].update({"index": index + 1})
            await super().send_message()
            return False

        else:
            index: int = CLIENT_INFO[self.chat_id].get("index") - 1
            CLIENT_INFO[self.chat_id]["data"].update({self.fields[index]: self.client_response})

            await self.post_process()
            CLIENT_INFO[self.chat_id].update({"index": 0, "data": {}})
            self.bot_markup = None
            await super().send_message()
            return True


    async def post_process(self) -> bool:
        pass


class ReceiverWithInlineMarkup(ReceiverBasic):
    def __init__(self, types, **kwargs):
        super(ReceiverWithInlineMarkup, self).__init__(types=types, **kwargs)
        self.bot_markup = quick_markup(values=kwargs.get("inline_json", {}), row_width=kwargs.get("row_width", 2))
