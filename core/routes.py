from functools import partial
from main import bot
from core.config import ALLOWED_CHAT_TYPE


# temporarily save the client information
CLIENT_INFO: dict = {}

def callback_connector(view,
                       func=lambda callback: True,
                       set_route:str=None,
                       allowed_route:str=None,
                       **kwargs):


    bot.callback_query_handler(func=func,
                               **kwargs)(partial(view, set_route=set_route, allowed_route=allowed_route))


def command_connector(view,
                      commands:list=["start"],
                      set_route:str=None,
                      allowed_route:str=None, **kwargs):



    bot.message_handler(commands=commands,
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(partial(view, set_route=set_route, allowed_route=allowed_route))


def message_connector(view,
                      func=lambda message: True,
                      set_route:str=None,
                      allowed_route:str=None,
                      **kwargs):


    bot.message_handler(func=func,
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(partial(view, set_route=set_route, allowed_route=allowed_route))


def route_assign(client_info:dict, chat_id:int, set_route:str=None) -> None:
    if client_info is None:
        CLIENT_INFO.update({chat_id: {"route": "", "info": {}, "data": {}}})

    if set_route is not None:
        CLIENT_INFO[chat_id].update({"route": set_route})
    return None


def route_check(client_info:dict, allowed_route:str=None) -> None:
    route: str | None = client_info.get("route", None) if client_info is not None else None

    if allowed_route is not None and allowed_route != route:
        raise ValueError(f"Mismatched Routes: allowed_route - '{allowed_route}', your_route: '{route}'")

    return None


def route_process(message=None, callback=None, allowed_route:str=None, set_route:str=None):
    if message is None and callback is None:
        raise ValueError("check_routes needs one of 'message' or 'callback' as a parameter.")

    chat_id: int = message.from_user.id if message is not None else callback.from_user.id
    client_info: dict | None = CLIENT_INFO.get(chat_id, None)

    route_check(client_info=client_info, allowed_route=allowed_route)
    route_assign(client_info=client_info, chat_id=chat_id, set_route=set_route)
    return None