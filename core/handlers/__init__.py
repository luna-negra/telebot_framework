from datetime import datetime
from telebot.types import Message


class MessageReceiver:
    """
    MessageReceiver:
    this class is charge of receiving message from client.

    THIS IS A TEMPLATE CLASS. DO NOT USE IT DIRECTLY.
    # Deprecated
    """

    def __init__(self, message):
        self.message = message
        self.request_user = self.message.from_user
        self.chat_id: int = self.request_user.id
        self.message_id: int = self.message.id
        self.timestamp: int = self.message.date
        self.rcv_datetime: datetime = datetime.fromtimestamp(self.timestamp)
        self.client_response: str = self.message.text


    async def get_message(self):
        pass


class CallBackReceiver:
    """
    CallBackReceiver:
    this class is charge of receiving callback data from client.

    THIS IS A TEMPLATE CLASS. DO NOT USE IT DIRECTLY.
    # Deprecated
    """

    def __init__(self, callback):
        self.callback = callback
        self.message = self.callback.message
        self.request_user = self.callback.from_user
        self.chat_id: int = self.request_user.id
        self.callback_id: int =self.callback.id
        self.message_id: int = self.message.id
        self.timestamp: int = self.message.date
        self.rcv_datetime: datetime = datetime.fromtimestamp(self.timestamp)
        self.client_response: str = self.callback.data


    async def get_callback(self):
        pass



class Receiver:
    def __init__(self, types):
        self.types = types
        self.request_user = self.types.from_user
        self.chat_id = self.types.from_user.id
        self.callback_id: int = None if type(self.types) == Message else self.types.id
        self.message_id: int = self.types if type(self.types) == Message else self.types.message
        self.timestamp: int = self.types.date if type(self.types) == Message else datetime.timestamp(datetime.now())
        self.rcv_datetime: datetime = datetime.fromtimestamp(self.timestamp)
        self.client_response = self.types.text if type(self.types) == Message else self.types.data

    async def get_client_data(self):
        pass

    async def send_message(self):
        pass