import re
from telebot.types import (CallbackQuery,
                           ForceReply,
                           InlineKeyboardMarkup,)
from telebot.util import quick_markup
from telebot.asyncio_helper import ApiTelegramException
from core.handlers import *
from core.routes import CLIENT_INFO
from core.config import SECRET_MODE


class ReceiverBasic(Receiver):
    """
    ReceiverBasic:
    This class will give message, responding to telegram user's request.
    This class inherits Receiver class.

    :param types: message or callback. Types should be assigned during creating instance of handler class in project/views.py
    :kwargs:
      - bot_text: content text contained in message that the bot will send to telegram user. Default is None
      - bot_markup: markup contained in message that the bot will send to telegram user. Default is None.
      - remove_user_msg: bool value to decide to remove previous all user messages in chat room. Default is False(not remove)
      - route: set the telegram user's route in your bot application.

    Use this class when you need to get a telegram user's request and just send a simple message with overriding send_message()
    """

    def __init__(self, types, **kwargs):
        super(ReceiverBasic, self).__init__(types=types)
        self.bot_text: str | None = kwargs.get("bot_text", None)
        self.bot_markup = kwargs.get("bot_markup", None)
        self.remove_user_msg = kwargs.get("remove_prev_msg", False)
        self.route = kwargs.get("route", None)
        if self.route is not None:
            CLIENT_INFO[self.chat_id].update({"route": self.route})

    async def send_message(self) -> None:
        """
        send_message:
        this method will make bot send message with bot_text to telegram user.
        or use as a forking point with if-else condition by overriding this method.

        :return: None
        """

        if await self._remove_prev_message():
            await self.bot.send_message(chat_id=self.chat_id,
                                        text=self.bot_text,
                                        reply_markup=self.bot_markup)
        return None

    async def _remove_prev_message(self) -> bool:
        """
        _remove_prev_message:
        This method decides whether it remove previous messages including InlineMarkup after user selection.

        if self.remove == True: remove all bots messages and user messages.
        else:                   remove all user messages(with text) only.

        :return: bool
        """

        if type(self.types) == CallbackQuery:
            # send user's selection to telegram bot.
            await self.bot.answer_callback_query(callback_query_id=self.callback_id)

            # if self.bot_text is None, remove previous buttons and pop up new Button on where previous button existed.
            if self.bot_text is None:
                await self.bot.edit_message_reply_markup(chat_id=self.chat_id,
                                                         message_id=self.message_id,
                                                         reply_markup=self.bot_markup or InlineKeyboardMarkup())
                return False

            if SECRET_MODE:
                # remove previous message with bot_text and new buttons.
                await self.__remove_messages()

                # edit answer_callback_query with new markup.
                try:
                    await self.bot.edit_message_reply_markup(chat_id=self.chat_id,
                                                        message_id=self.message_id,
                                                        reply_markup=self.bot_markup or InlineKeyboardMarkup())

                # if there is no answer_callback_query, will send default self.bot_text and self.markup in this class.
                # e.g: if a method in views.py is called manually so that there is no callback information,
                except ApiTelegramException:
                    pass

        elif type(self.types) == Message:
            if SECRET_MODE:
                await self.__remove_messages()

            else:
                if self.remove_user_msg:
                    try:
                        await self.bot.delete_message(chat_id=self.chat_id, message_id=self.message_id)

                    except ApiTelegramException:
                        pass

        return True

    async def __remove_messages(self) -> None:
        """
        __remove_messages:
        this method is charge of only removing previous 3 messages left on chat room.

        :return:
        """
        try:
            # remove previous bot message
            await self.bot.delete_message(chat_id=self.chat_id, message_id=self.message_id)
            await self.bot.delete_message(chat_id=self.chat_id, message_id=self.message_id - 1)
            await self.bot.delete_message(chat_id=self.chat_id, message_id=self.message_id - 2)

        except ApiTelegramException:
            pass

        return None


class ReceiverWithForceReply(ReceiverBasic):
    """
    ReceiverWithForceReply:
    This class will give ForceReply markup message, responding to telegram user's request.
    This class inherits ReceiverBasic class.

    Use this class when you need to get several user's input consecutively. for example,
    - 'Sign in' requires username and password from user.
    - 'Sign Up' requires username, password, first_name and last_name
    """

    class Meta:
        """
        This class is an inner Meta class for ReceiverWithForceReply.

        * fields: fields name that the user must input.
        * fields_text: fields text to guide telegram user.
        * fields_regex: fields regex that telegram user must input in a specific field.
        * fields_error_msg: error text to inform telegram user of regex mismatch.
        """

        fields: list | tuple | None = None
        fields_text: str | list | tuple | None = None
        fields_regex: str | list | tuple | None = None
        fields_error_msg: str | list | tuple | None = None

    def __init__(self, types, **kwargs):
        super(ReceiverWithForceReply, self).__init__(types=types, **kwargs)
        self.client_data = CLIENT_INFO[self.chat_id]["data"]
        self.bot_markup = ForceReply()

        self.fields = getattr(self.Meta, 'fields', ())
        if not isinstance(self.fields, (tuple, list)):
            raise ValueError("[ReceiverWithForceReply] 'fields' in Meta class must be list or tuple")

        if len(self.fields) == 0:
            raise AttributeError("[ReceiverWithForceReply] 'fields' in Meta class must have at least one field name")

        self.fields_text = getattr(self.Meta, 'fields_text', {field: field for field in self.fields})
        self.fields_regex = getattr(self.Meta, 'fields_regex', {field: ".*" for field in self.fields})
        self.fields_error_msg = getattr(self.Meta, 'fields_error_msg', {field: f"'{field}' does not match regex." for field in self.fields})

    async def get_client_data(self) -> bool:
        """
        get_client_data:
        This method gets severer inputs from telegram user, referring to the Meta.field.
        -  send message to telegram user to guide what text user must input.
        -  get user input for each field
        -  check the regex with user input.
        -  save relative data in "data" in CLIENT_INFO

        :return: bool
        """

        flag = False
        index: int = CLIENT_INFO[self.chat_id].get("index")

        # Receiving User Input.
        # Condition ignore index 0 because index 0 is a callback.data, not a message.text
        if index != 0 :
            pre_index = index - 1
            pre_field = self.fields[pre_index]
            regex_list = self.fields_regex.get(pre_field, [".*"])
            error_msg = self.fields_error_msg.get(pre_field, f"'{pre_field}' is not satisfying regex.")

            if not isinstance(regex_list, (list, tuple)):
                regex_list = [regex_list]

            if not isinstance(error_msg, (list, tuple)):
                error_msg = [error_msg]

            # check regex with telegram user's input.
            for regex in regex_list:
                inner_index = regex_list.index(regex)
                if not re.search(pattern=regex, string=self.client_response):
                    self.bot_text = error_msg[0] if len(error_msg) != len(regex_list) else error_msg[inner_index]
                    self.bot_markup = None
                    CLIENT_INFO[self.chat_id].update({"index": 0, "data": {}})
                    flag = True
                    break

            # if regex is not match.
            if flag:
                await self.send_message()
                CLIENT_INFO[self.chat_id].update({"index": index - 1})
                index -= 1
                self.bot_markup = ForceReply()
                flag = False

            else:
                # save user's input to CLIENT_INFO, especially in "data"
                CLIENT_INFO[self.chat_id]["data"].update({pre_field: self.client_response})

        # Index is not equal to length of fields in Meta class.
        if index != len(self.fields):
            field = self.fields[index]
            self.bot_text = self.fields_text[field]

            # update index number for referring.
            CLIENT_INFO[self.chat_id].update({"index": index + 1})

        # if user gave input for last field,
        else:
            index: int = CLIENT_INFO[self.chat_id].get("index") - 1

            # save user's last input to CLIENT_INFO[self.chat_id]["data"]
            CLIENT_INFO[self.chat_id]["data"].update({self.fields[index]: self.client_response})

            # process with user data. it must be overridden by developer.
            await self.post_process()

            # reset CLIENT_INFO and bot_markup.
            CLIENT_INFO[self.chat_id].update({"index": 0, "data": {}})
            self.bot_markup = None
            flag = True

        await self.send_message()
        return flag

    async def post_process(self):
        """
        post_process:
        This method is charge of processing user input saved in CLIENT_INFO[self.chat_id]["data"]
        Developer must override this method for post job. for example: API Calling

        :return:
        """

        pass

    async def send_message(self) -> None:
        """
        send_message:
        This method will make bot send message to telegram user.
        It can remove user message before sending bot message to telegram user.

        :return: None
        """

        await super().send_message()
        return None


class ReceiverWithInlineMarkup(ReceiverBasic):
    """
    ReceiverWithInlineMarkup:
    This class will give message with InlineMarkupButton, responding to telegram user's request.
    This class inherits ReceiverBasic class.

    Use this class if you need to send several InlineMarkupButtons to telegram user.
    """

    class Meta:
        """
        This class is an inner Meta class for ReceiverWithForceReply.

        * fields: InlineMarkupButton text that show to telegram user.
        * fields_callback: callback data behind each InlineMarkupButton
        * fields_url: url string behind each InlineMarkupButton.
        """

        fields = None
        fields_callback = None
        fields_url = None

    def __init__(self, types, **kwargs):
        super(ReceiverWithInlineMarkup, self).__init__(types=types, **kwargs)
        self.fields = getattr(self.Meta, 'fields', ())

        if self.fields is not None:
            self.fields_callback = getattr(self.Meta, "fields_callback", {field: field.lower().replace(" ", "_") for field in self.fields})
            self.fields_url = getattr(self.Meta, "fields_url", {field: None for field in self.fields})
            self.values = {key: {
                "callback_data": self.fields_callback.get(key, key.lower().replace(" ", "_")),
                "url": self.fields_url.get(key, None),
            } for key in self.fields}
            self.bot_markup = quick_markup(values=self.values, row_width=kwargs.get("row_width", 2))

    async def get_client_data(self) -> any:
        """
        get_client_data:
        This method is responsible to send message with InlineMarkupButton.

        :return: any
        """

        await self.pre_process()
        await super().send_message()
        return await self.post_process()

    async def post_process(self):
        """
        post_process:
        This method is charge of processing user input saved in CLIENT_INFO[self.chat_id]["data"]
        Developer must override this method for post job. for example: API Calling

        :return:
        """

        pass

    async def pre_process(self) -> None:
        """
        pre_process
        This class is charge of setting self.bot_text to print out text information.

        Please set self.bot_text by overriding this method.

        :return: None
        """

        pass


class ResultShowingWithInlineMarkup(ReceiverWithInlineMarkup):
    """
    ResultShowingWithInlineMarkup:

    If you want to show some result to telegram user and user have to check before doing next process,
    this class will provide 'Continue' button on the chat room.
    """

    class Meta:
        fields = ["Continue"]
        fields_callback: dict = {
            "Continue": None
        }

    def __init__(self, types, link_route: str, **kwargs):
        self.Meta.fields_callback.update({self.Meta.fields[0]: link_route})
        super(ResultShowingWithInlineMarkup, self).__init__(types, **kwargs)

    async def send_message(self) -> None:
        """
        send_message:
        send_message with result that comes from the last process in method self.pre_process().

        :return: None
        """

        await self.pre_process()
        await super().send_message()
        return None
