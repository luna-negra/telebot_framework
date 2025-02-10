from core.handlers import MsgReceiver


class MessageForceReply(MsgReceiver):
    async def get_message(self) -> None:
        return None
