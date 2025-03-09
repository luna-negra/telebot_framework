from telebot.types import InputPollOption
from core.handlers.handlers import ResultShowingWithInlineMarkup



class PollTest(ResultShowingWithInlineMarkup):
    async def send_message(self) -> None:
        if await self._remove_prev_message():
            await self.bot.send_poll(chat_id=self.chat_id,
                                     question="Poll Query",
                                     options=[InputPollOption(text="option1"),
                                              InputPollOption(text="option2"),
                                              InputPollOption(text="option3")],
                                     reply_markup=self.bot_markup)
    # 2025.03.09 Now Testing.