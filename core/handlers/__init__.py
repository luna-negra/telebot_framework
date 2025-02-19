from datetime import datetime
from telebot.types import Message


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