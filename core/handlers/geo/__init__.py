from urllib.parse import urlencode
from requests import get as requests_get
from telebot.types import ForceReply
from core.handlers.handlers import ResultShowingWithInlineMarkup


class ReceiverWithLocation(ResultShowingWithInlineMarkup):
    """
    ReceiverWithLocation:

    this class is responsible for sending location of telegram user.
    when user sends its location on Attachment > location, telegram can grap the location information(latitude and longitude).

    this class can be used to update current location or record travel routes and so on.
    user must send its location manually.
    """

    def __init__(self, types, **kwargs):
        super(ReceiverWithLocation, self).__init__(types, **kwargs)
        self.location = None


    async def get_location(self) -> bool:
        """
        this method is charge of sending preamble message and receiving user's current location.
        you can reprocess the location information with self.location:dict

        :return: bool
        """

        if getattr(self.types, "location", None) is not None:
            self.location = self.types.location.to_dict()
            await self.post_process()

            await self.bot.send_message(chat_id=self.chat_id,
                                        text=self.bot_text)
            return True

        await super().send_message()
        return False


class ReceiverWithRTLocation:
    # designing from 2025.03.10...
    pass


class SenderWithLocation(ResultShowingWithInlineMarkup):
    def __init__(self, types, **kwargs):
        super(SenderWithLocation, self).__init__(types, **kwargs)
        self.latitude = None
        self.longitude = None

    async def pre_process(self):
        pass

    async def send_message(self):
        await self.pre_process()

        if self.latitude is None or self.longitude is None:
            raise ValueError("[ERROR] Fail to get location information.")

        if not isinstance(self.latitude, float) or not isinstance(self.longitude, float):
            raise ValueError("[Error] Latitude or longitude must be float.")

        await self.bot.send_location(chat_id=self.chat_id,
                                     latitude=self.latitude,
                                     longitude=self.longitude,
                                     reply_markup=self.bot_markup)
        return None


class SendWithLocationName(ResultShowingWithInlineMarkup):

    GEO_INFO_API_URL: str = "https://nominatim.openstreetmap.org/search?"

    def __init__(self, types, **kwargs):
        super(SendWithLocationName, self).__init__(types, **kwargs)
        self.latitude = None
        self.longitude = None

    async def send_message(self):
        if getattr(self.types, "message", None) is None:
            await self._remove_prev_message()
            await self.post_process()
            return True

        await super().send_message()
        self.bot_markup = ForceReply()
        await self.bot.send_message(chat_id=self.chat_id,
                                    text="* Postal Number, Address or Site Name:",
                                    reply_markup=ForceReply())
        return False

    async def post_process(self):
        headers = {"User-Agent": "telebot_framework"}
        params = {
            "q": self.client_response,
            "format": "jsonv2",
            "limit": 4
        }
        response = requests_get(url=self.GEO_INFO_API_URL + urlencode(params),
                                headers=headers)

        if response.status_code == 200 and len(response.json()) != 0:
            location = response.json()[0]
            address = location.get("display_name")
            location_type = location.get('type')
            self.latitude = location.get("lat")
            self.longitude = location.get("lon")
            text = f"* Location: {self.client_response}\n* Address: {address}\n * Type: {location_type}"

            if await self._remove_prev_message():
                await self.bot.send_message(chat_id=self.chat_id,
                                            text=text)
                await self.bot.send_location(chat_id=self.chat_id,
                                             latitude=self.latitude,
                                             longitude=self.longitude,
                                             reply_markup=self.bot_markup)

        else:
            self.bot_text = "Fail to get a location info."
            await self.bot.send_message(chat_id=self.chat_id,
                                        text=self.bot_text,
                                        reply_markup=self.bot_markup)
        return None