from core.handlers.handlers import (ReceiverBasic,
                                    ReceiverWithForceReply,)


class SigninBasic(ReceiverWithForceReply):
    pass


class SignOut(ReceiverBasic):
    pass


class SignUp(ReceiverWithForceReply):
    pass


class DeleteAccount(ReceiverWithForceReply):
    pass

