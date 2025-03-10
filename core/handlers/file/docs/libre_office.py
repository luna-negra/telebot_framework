from core.handlers.file.docs import ReceiverWithDocs


class ReceiverWithWriterFile(ReceiverWithDocs):
    async def validate_file(self) -> None:
        if not self.file_type == "application/vnd.oasis.opendocument.text":
            raise ValueError(f"[ERROR] File must be a Writer. You uploaded '{self.file_type}'")

        return None


class ReceiverWithCalcFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.oasis.opendocument.spreadsheet":
            raise ValueError(f"[ERROR] File must be a Calc. You uploaded '{self.file_type}'")

        return None


class ReceiverWithImpressFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.oasis.opendocument.presentation":
            raise ValueError(f"[ERROR] File must be an Impress. You uploaded '{self.file_type}'")

        return None
