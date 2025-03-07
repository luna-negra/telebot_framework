from os import makedirs
from shutil import rmtree
from core.handlers.file.docs import (ReceiverWithDocs,
                                     ResultShowingWithInlineMarkup,)


class ReceiverWithImage(ReceiverWithDocs):
    """
    ReceiverWithImage:

    this class is charge of getting uploaded image from telegram user.
    """

    def __init__(self, types, **kwargs):
        super(ReceiverWithImage, self).__init__(types, **kwargs)
        self.receive_type = "photo"

    async def get_uploaded_file(self) -> bool:

        if getattr(self.types, "photo", None):
            file_id = self.types.photo[-1].file_id

            try:
                await self.validate_file()

            except ValueError as e:
                self.bot_text = e
                self.bot_markup = None
                await super().send_message()
                return True

            else:
                get_file = await self.bot.get_file(file_id=file_id)
                self.file = await self.bot.download_file(file_path=get_file.file_path)
                self.bot.send_photo()
                await self.post_process()
                return True

        await super().send_message()
        return False


# SenderWithImage
# How can I send image after getting data from API server?
class SenderWithImage(ResultShowingWithInlineMarkup):
    """
    """

    FILE_STORAGE_FOLDER: str = "core/tmp_storage"

    def __init__(self, types, filename:str, **kwargs):
        super(SenderWithImage, self).__init__(types=types, **kwargs)
        self.filename = filename
        self.filepath = f"{SenderWithImage.FILE_STORAGE_FOLDER}/{self.chat_id}/{filename}"
        self.content = None

    async def __create_file(self, content) -> None:
        """
        this method is charge of producing download file with content from pre_process.

        #please use it at the end of pre_process() method.
        #you can insert your own logic in pre_process without using this method to create a file.

        :param content: content that you would like to write in a file.
        :return: None
        """

        while True:
            try:
                with open(self.filepath, mode="wb") as file:
                    file.write(content)
                    break

            except FileNotFoundError:
                makedirs(name="/".join(self.filepath.split("/")[:-1]), exist_ok=True)

        return None


    async def pre_process(self) -> None:
        """
        create a content that you want to write down on download file by overriding this method.

        :return: None
        """

        return None

    async def send_message(self):
        """
        this method sends file in specific folder from bot to user.

        :return:
        """

        # Save content to the filepath.
        await self.pre_process()

        if self.content is not None:
            await self.__create_file(content=self.content)

            # Remove original markup for bot_text and move it to under the file message.
            tmp = self.bot_markup
            self.bot_markup = None
            if await self._remove_prev_message():
                await self.bot.send_message(chat_id=self.chat_id,
                                            text=self.bot_text,
                                            reply_markup=self.bot_markup)

            # send message with file download link and markup
            with open(self.filepath, mode="rb") as f:
                await self.bot.send_photo(chat_id=self.chat_id,
                                          photo=f,
                                          reply_markup=tmp)

            await self.__remove_file()

        else:
            self.bot_text = "[ERROR] There is no content to write down."
            await super().send_message()

        return None


    async def __remove_file(self):
        """
        this method removes download file which was temporarily stored in FILE_STORAGE_FOLDER.

        :return: None
        """

        rmtree("/".join(self.filepath.split("/")[:-1]))
        return None