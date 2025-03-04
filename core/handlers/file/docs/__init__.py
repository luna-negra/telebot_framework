from pathlib import Path
from core.config import FILE_STORAGE_FOLDER
from core.handlers.handlers import (ResultShowingWithInlineMarkup,
                                    CLIENT_INFO)



class ReceiverWithDocs(ResultShowingWithInlineMarkup):
    """
    ReceiverWithDocs:

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
    file must be placed in specific folder(file_storage)  before being sent.
    """

    def __init__(self, types, rel_filepath:str, **kwargs):
        self.filepath = None
        self.rel_filepath = rel_filepath
        self.root_storage = FILE_STORAGE_FOLDER
        super(SenderWithDocs, self).__init__(types=types, **kwargs)


    async def create_file(self, content) -> None:
        # add logic to create a non exist folder

        with open(f"{self.root_storage}/{self.rel_filepath}", mode="w", encoding="utf-8") as file:
            file.write(str(content))

        return None


    async def pre_process(self):
        """
        create a file on file_storage folder by overriding this method with self.create_file()

        :return:
        """

        pass

    async def send_message(self):
        """
        this method sends file in specific folder from bot to user.

        :return:
        """

        await self.pre_process()
        for path in Path(self.root_storage).rglob(f"*{self.rel_filepath}"):
            if path.is_file():
                self.filepath = f"{FILE_STORAGE_FOLDER}/{self.rel_filepath}"
                break

        if self.filepath is None:
            self.bot_text = f"[Error] File '{self.rel_filepath.split("/")[-1]}' does not exist on file_storage"
            await super().send_message()
            return None

        tmp = self.bot_markup
        self.bot_markup = None
        await super().send_message()
        with open(self.filepath, mode="rb") as file:
            await self.bot.send_document(chat_id=self.chat_id,
                                         document=file,
                                         reply_markup=tmp)

        return None

    async def __get_file(self) -> None:

        return None
