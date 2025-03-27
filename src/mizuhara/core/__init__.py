

class UserInfo:
    """
    UserInfo:

    this class is charge of saving telegram user's information in mizuhara.core.routes.CLIENT_INFO
    """

    def __init__(self, **kwargs):
        self.route: str = ""
        self.info: dict = {}
        self.data: dict = {}
        self.index: int = 0
        self.page: int = 0
        self.is_signin: bool = False
        self.language: str|None = None

    def get(self, key: str, default=None):
        return self.__dict__.get(key, default)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)