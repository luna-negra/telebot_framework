from datetime import datetime


class MsgReceiver:
    """
    MsgReceiver:
    this class is charge of receiving message from client.

    THIS IS A TEMPLATE CLASS. DO NOT USE IT DIRECTLY.
    """

    def __init__(self, message):
        self.message = message
        self.request_user = message.from_user
        self.chat_id: int = self.request_user.id
        self.message_id: int = message.id
        self.timestamp: int = message.date
        self.rcv_datetime: datetime = datetime.fromtimestamp(self.timestamp)
        self.client_text: str = message.text


    async def send_message(self):
        pass


class CallbackReceiver:
    """
    CallbackReceiver:
    this class is charge of receiving callback data from client.

    THIS IS A TEMPLATE CLASS. DO NOT USE IT DIRECTLY.
    """

    def __init__(self, callback):
        self.callback = callback
        self.message = self.callback.message
        self.request_user = self.callback.from_user
        self.chat_id: int = self.request_user.id
        self.callback_id: int =self.callback.id
        self.message_id: int = self.message.id
        self.callback_data: str = callback.data


    async def get_callback(self, callback):
        pass