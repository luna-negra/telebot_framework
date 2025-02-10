from main import bot, logger
from core.config import ALLOWED_CHAT_TYPE


# temporarily save the client information
CLIENT_INFO: dict = {}

def connector_callback(view,
                       set_route:str=None,
                       allowed_route:str=None,
                       callback_data:str=None,
                       **kwargs):
    """
    connector_callback:
    mapper function between route and view.

    :param view: function class that you want to map with specific route
    :param set_route: assign route to view function
    :param allowed_route: route that the client can access.
    :param callback_data: set the callback data to response with InlineKeyboardButton
    :param kwargs:
    :return:
    """

    bot.callback_query_handler(func=lambda callback: route_process(reply=callback,
                                                                   set_route=set_route,
                                                                   allowed_route=allowed_route,
                                                                   callback_data=callback_data,),
                               **kwargs)(view)


def connector_command(view,
                      commands:list=["start"],
                      set_route:str=None,
                      allowed_route:str=None,
                      **kwargs):

    if set_route is None:
        raise ValueError("you have to assign 'set_route' to use 'command_connector'")

    bot.message_handler(commands=commands,
                        func=lambda message: route_process(reply=message,
                                                           set_route=set_route,
                                                           allowed_route=allowed_route),
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(view)


def connector_message(view,
                      set_route:str=None,
                      allowed_route:str=None,
                      **kwargs):

    bot.message_handler(func=lambda message: route_process(reply=message,
                                                           set_route=set_route,
                                                           allowed_route=allowed_route),
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(view)



def __assign_route(client_info:dict, chat_id:int, set_route:str) -> None:
    if client_info is None:
        CLIENT_INFO.update({chat_id: {"route": "", "info": {}, "data": {}}})

    if set_route is not None:
        CLIENT_INFO[chat_id].update({"route": set_route})
    return None


def __check_callback(reply, callback_data:str) -> bool:
    condition: bool = True
    if callback_data is not None:
        try:
            condition = reply.data == callback_data

        except Exception as e:
            print(e)

    return condition


def __check_route(client_info:dict, allowed_route:str) -> bool:
    condition: bool = True
    client_route: str | None = client_info.get("route", None) if client_info is not None else None
    if allowed_route is not None:
        condition = client_route == allowed_route

    return condition


def route_process(reply,
                  set_route:str =None,
                  allowed_route:str=None,
                  callback_data:str=None,) -> bool:

    chat_id: int = reply.from_user.id
    client_info: dict | None = CLIENT_INFO.get(chat_id, None)
    condition1: bool = __check_route(client_info=client_info, allowed_route=allowed_route)
    condition2: bool = __check_callback(reply=reply, callback_data=callback_data)

    if condition1 and condition2:
        if set_route is not None:
            __assign_route(client_info=client_info, chat_id=chat_id, set_route=set_route)
        return True

    return False
