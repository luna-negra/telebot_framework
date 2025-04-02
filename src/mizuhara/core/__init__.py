

class UserInfo:
    """
    UserInfo:

    this class is charge of saving telegram user's information in mizuhara.core.routes.CLIENT_INFO
    """

    def __init__(self, types, **kwargs):
        self.chat_info = {
            "msg_name": "TLGR",
            "chat_id": str(types.from_user.id),
            "is_signed_in": True
        }
        self.data: dict = {}
        self.info: dict = {}
        self.index: int = 0
        self.language: str = types.from_user.language_code
        self.is_signin: bool = False
        self.page: int = 0
        self.route: str = ""

    def get(self, key: str, default=None):
        return self.__dict__.get(key, default)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)