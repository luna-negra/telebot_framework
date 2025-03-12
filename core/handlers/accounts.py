from core.handlers.handlers import (ReceiverBasic,
                                    ReceiverWithForceReply,
                                    CLIENT_INFO)


class SignInBasic(ReceiverWithForceReply):
    class Meta:
        fields = ["email", "password"]
        #fields_text = {
        #    "email": "[Sign In]\n* Input Email",
        #    "password": "[Sign In]\n* Input Password",
        #}
        fields_text = {
            "email": "signin_email",
            "password": "signin_password",
        }
        fields_regex = {
            "email": "^.+@.+\\..+$",
        }
        fields_error_msg = {
            "email": "Not an Email Format",
        }

    def __init__(self, types, **kwargs):
        super(SignInBasic, self).__init__(types, **kwargs)

    async def get_client_data(self) -> bool:
        if not CLIENT_INFO[self.chat_id].get("is_signin"):
            return await super().get_client_data()

        else:
            await self.bot.send_message(chat_id=self.chat_id, text="[WARNING]\nYou are already signed in.")
            return True


class SignOut(ReceiverBasic):
    async def pre_process(self) -> bool:
        if not CLIENT_INFO[self.chat_id].get("is_signin"):
            self.bot_text = "[WARNING]\nYou are already signed out."
            return False
        return True

    async def send_message(self) -> None:
        if await self.pre_process():
            await self.post_process()

        await super().send_message()
        return None

    async def post_process(self):
        pass


class SignUp(ReceiverWithForceReply):
    class Meta:
        fields = ["email", "password"]
        fields_text = {
            "email": "[Sign Up]\n* Input Email",
            "password": "[Sign Up]\n* Input Password",
        }
        fields_regex = {
            "email": ("^.*@.+\\..+$", "^.+@.+\\.com"),
            "password": (
                "[A-Z]+",
                "[a-z]+",
                "[0-9]+",
                "[!@#$%^&*()_+\\-=]+",
            )
        }
        fields_error_msg = {
            "email": "Not an Email Format",
            "password": (
                "Must contain at least one Upper",
                "Must contain at least one Lower",
                "Must contain at least one digit",
                "Must contain at least one special",
            )
        }

    def __init__(self, types, **kwargs):
        super(SignUp, self).__init__(types, **kwargs)


class DeleteAccount(ReceiverWithForceReply):
    class Meta:
        fields = ["password"]
        fields_text = {
            "password": "[Delete Account]\n* Input Password to delete your account."
        }

    def __init__(self, types, **kwargs):
        super(DeleteAccount, self).__init__(types, **kwargs)
