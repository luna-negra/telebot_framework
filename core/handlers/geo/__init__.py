from core.handlers.handlers import ResultShowingWithInlineMarkup
from core.handlers.handlers import SenderWithBasic


class ReceiverWithLocation(ResultShowingWithInlineMarkup):
    """
    ReceiverWithLocation:

    this class is responsible for sending location of telegram user.
    when user sends its location on Attachment > location, telegram can grap the location information(latitude and logitude).

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


class SenderWithLocation(SenderWithBasic):
    # send location info with longitude and latitude
    # designing from 2025.03.10...
    pass


class SenderWithSearchedLocation(SenderWithLocation):
    # send location information that user want to search the name of site or area.
    # designing from 2025.03.10
    pass