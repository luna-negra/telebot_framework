from core.handlers.handlers import (ReceiverBasic,
                                    ResultShowingWithInlineMarkup,
                                    CLIENT_INFO)


class ReceiverWithDocs(ResultShowingWithInlineMarkup):
    class Meta:
        fields = ["Cancel"]
        fields_callback: dict = {
            "Continue": None
        }

    def __init__(self, types, **kwargs):
        self.file: bytes|None = None
        self.file_name: str|None = None
        self.file_type: str|None = None
        super(ReceiverWithDocs, self).__init__(types, **kwargs)

    async def get_uploaded_file(self) -> bool:
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
        pass

    async def post_process(self):
        pass


class ReceiverWithCSVFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "text/comma-separated-values":
            raise ValueError(f"[ERROR] File must be a CSV. You uploaded '{self.file_type}'")

        return None


class ReceiverWithJsonFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "application/json":
            raise ValueError(f"[ERROR] File must be a Json. You uploaded '{self.file_type}'")

        return None


class ReceiverWithMarkdownFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "text/markdown":
            raise ValueError(f"[ERROR] File must be a Markdown. You uploaded '{self.file_type}'")

        return None


class ReceiverWithPDFFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "application/pdf":
            raise ValueError(f"[ERROR] File must be a PDF. You uploaded '{self.file_type}'")

        return None


class ReceiverWithTextFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "text/plain":
            raise ValueError(f"[ERROR] File must be a text. You uploaded '{self.file_type}'")

        return None


class ReceiverWithXMLFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "application/xml":
            raise ValueError(f"[ERROR] File must be an XML. You uploaded '{self.file_type}'")

        return None


class ReceiverWithYamlFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "application/octet-stream":
            raise ValueError(f"[ERROR] File must be a YAML. You uploaded '{self.file_type}'")

        return None


class ReceiverWithZipFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "application/zip":
            raise ValueError(f"[ERROR] File must be a zip. You uploaded '{self.file_type}'")

        return None


class SenderWithDocs(ReceiverBasic):
    pass
