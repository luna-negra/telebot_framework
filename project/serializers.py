# please import handlers classes in core.handlers
# and inherit one of them to your custom handler serializer classes.
from core.handlers.callback_handlers import CallbackReceiverWithForceReply
from core.handlers.command_handlers import *
from core.handlers.message_handlers import *
from core.routes import CLIENT_INFO
from execute import bot


# please write down your code below.
class Main(CommandReceiverWithInlineMarkup):
    def __init__(self, message, **kwargs):
        super(Main, self).__init__(message=message, **kwargs)
        self.bot_text: str = "Welcome to Main.\n"
        inline_json: dict = {}
        signed_in_flag: bool = False if CLIENT_INFO[self.chat_id].get("info") == {} else True

        if signed_in_flag:
            self.bot_text += "You are already signed in."
            inline_json.update({
                "Account": {"callback_data": "account"},
                "Settings": {"callback_data": "settings"},
                "Sign Out": {"callback_data": "signout"},
            })

        else:
            self.bot_text += "You have to sign in or sign up."
            inline_json.update({
                "Sign In": {"callback_data": "signin"},
                "Sign Up": {"callback_data": "signup"},
            })

        self.bot_markup = quick_markup(values=inline_json)


class Signin(CallbackReceiverWithForceReply):
    def __init__(self, callback, **kwargs):
        super(Signin, self).__init__(callback=callback, **kwargs)


class SignInPrompt(MessageReceiverWithForceReply):
    def __init__(self, message, **kwargs):
        super(SignInPrompt, self).__init__(message=message, **kwargs)
        self.client_info: dict = CLIENT_INFO[self.chat_id]["data"]


    async def get_message(self) -> None:
        key: str = "username" if self.client_info.get("username", None) is None else "password"
        self.client_info.update({key: self.client_text})
        return None


    async def send_message(self) -> None:
        if self.client_info.get("password", None) is None:
            await super().send_message()

        else:
            print("CALL_API")

        return None