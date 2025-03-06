from shutil import rmtree
from os import makedirs
from core.handlers.handlers import (ResultShowingWithInlineMarkup,
                                    CLIENT_INFO)


class ReceiverWithDocs(ResultShowingWithInlineMarkup):
    """
    ReceiverWithFile:

    this class is charge of getting uploaded file from telegram user.
    """

    class Meta:
        """
        this Meta class creates InlineMarkupButton to provide Cancel button to telegram user,
        who does not want to upload his or her file after executing file uploading process.

        """

        fields = ["Cancel"]
        fields_callback: dict = {
            "Cancel": None
        }

    def __init__(self, types, **kwargs):
        self.file: bytes|None = None
        self.file_name: str|None = None
        self.file_type: str|None = None
        super(ReceiverWithDocs, self).__init__(types, **kwargs)

    async def get_uploaded_file(self) -> bool:
        """
        this method receives an uploaded file from telegram user, validates file,
        and does post process with uploaded file.

        :return: bool
        """

        if getattr(self.types, "document", None):
            file_info = self.types.document
            file_id = file_info.file_id
            self.file_name = file_info.file_name
            self.file_type = file_info.mime_type

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
                await self.post_process()
                return True

        await super().send_message()
        return False

    async def validate_file(self):
        """
        please override this method to validate uploaded file.
        if there is an error, please RAISE ERROR with 'ValueError'

        :return: bool
        """

        pass

    async def post_process(self):
        """
        please override this method if you need to do some work with uploaded file.

        :return: bool
        """
        pass


class ReceiverWithCSVFile(ReceiverWithDocs):
    """
    ReceiverWithDocs:

    this class is charge of getting uploaded 'CSV' file from telegram user.
    """

    async def validate_file(self) -> None:
        if not self.file_type == "text/comma-separated-values":
            raise ValueError(f"[ERROR] File must be a CSV. You uploaded '{self.file_type}'")

        return None


class ReceiverWithJsonFile(ReceiverWithDocs):
    """
    ReceiverWithDocs:

    this class is charge of getting uploaded 'Json' file from telegram user.
    """

    async def validate_file(self) -> None:
        if not self.file_type == "application/json":
            raise ValueError(f"[ERROR] File must be a Json. You uploaded '{self.file_type}'")

        return None


class ReceiverWithMarkdownFile(ReceiverWithDocs):
    """
    ReceiverWithDocs:

    this class is charge of getting uploaded 'markdown' file from telegram user.
    """

    async def validate_file(self) -> None:
        if not self.file_type == "text/markdown":
            raise ValueError(f"[ERROR] File must be a Markdown. You uploaded '{self.file_type}'")

        return None


class ReceiverWithPDFFile(ReceiverWithDocs):
    """
    ReceiverWithDocs:

    this class is charge of getting uploaded 'PDF' file from telegram user.
    """

    async def validate_file(self) -> None:
        if not self.file_type == "application/pdf":
            raise ValueError(f"[ERROR] File must be a PDF. You uploaded '{self.file_type}'")

        return None


class ReceiverWithTextFile(ReceiverWithDocs):
    """
    ReceiverWithDocs:

    this class is charge of getting uploaded 'text' file from telegram user.
    """

    async def validate_file(self) -> None:
        if not self.file_type == "text/plain":
            raise ValueError(f"[ERROR] File must be a text. You uploaded '{self.file_type}'")

        return None


class ReceiverWithXMLFile(ReceiverWithDocs):
    """
    ReceiverWithDocs:

    this class is charge of getting uploaded 'XML' file from telegram user.
    """

    async def validate_file(self) -> None:
        if not self.file_type == "application/xml":
            raise ValueError(f"[ERROR] File must be an XML. You uploaded '{self.file_type}'")

        return None


class ReceiverWithYamlFile(ReceiverWithDocs):
    """
    ReceiverWithDocs:

    this class is charge of getting uploaded 'YAML' file from telegram user.
    """

    async def validate_file(self) -> None:
        if not self.file_type == "application/octet-stream":
            raise ValueError(f"[ERROR] File must be a YAML. You uploaded '{self.file_type}'")

        return None


class ReceiverWithZipFile(ReceiverWithDocs):
    """
    ReceiverWithDocs:

    this class is charge of getting uploaded 'Zip' file from telegram user.
    """

    async def validate_file(self) -> None:
        if not self.file_type == "application/zip":
            raise ValueError(f"[ERROR] File must be a zip. You uploaded '{self.file_type}'")

        return None


class SenderWithDocs(ResultShowingWithInlineMarkup):
    """
    SenderWithDocs:

    this class is charge of sending file from bot to user.
    this class receives the data which would be written in document or file,
    and convert data into the string content for download file.

    the bot will send created file to telegram user.
    please use it to create analysis report or summary after collecting data.
    """

    FILE_STORAGE_FOLDER: str = "core/tmp_storage"

    def __init__(self, types, filename:str, **kwargs):
        super(SenderWithDocs, self).__init__(types=types, **kwargs)
        self.filename = filename
        self.filepath = f"{SenderWithDocs.FILE_STORAGE_FOLDER}/{self.chat_id}/{filename}"
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
                with open(self.filepath, mode="w", encoding="utf-8") as file:
                    file.write(str(content))
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
            await super().send_message()

            # send message with file download link and markup
            with open(self.filepath, mode="rb") as file:
                await self.bot.send_document(chat_id=self.chat_id,
                                             document=file,
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
