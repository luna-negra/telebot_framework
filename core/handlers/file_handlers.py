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

    async def get_uploaded_file(self):
        if getattr(self.types, "document", None):
            file_info = self.types.document
            file_id = file_info.file_id
            self.file_name = file_info.file_name
            self.file_type = file_info.mime_type

            try:
                await self.validate_file()

            except ValueError as e:
                self.bot_text = e

            else:
                get_file = await self.bot.get_file(file_id=file_id)
                self.file = await self.bot.download_file(file_path=get_file.file_path)
                await self.post_process()
                return None

        await super().send_message()
        return None

    async def validate_file(self):
        pass

    async def post_process(self):
        pass


class SenderWithDocs(ReceiverBasic):
    pass