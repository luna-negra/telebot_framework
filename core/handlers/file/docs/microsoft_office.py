from core.handlers.file.docs import (ReceiverWithDocs,
                                     CLIENT_INFO)


class ReceiverWithExcelFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise ValueError(f"[ERROR] File must be an Excel. You uploaded '{self.file_type}'")

        return None


class ReceiverWithPPTFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            raise ValueError(f"[ERROR] File must be an PPT. You uploaded '{self.file_type}'")


class ReceiverWithWordFile(ReceiverWithDocs):
    async def validate_file(self):
        if not self.file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            raise ValueError(f"[ERROR] File must be an Word. You uploaded '{self.file_type}'")

        return None
