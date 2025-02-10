from main import (bot,
                  logger)
from core.config import ALLOWED_CHAT_TYPE


# temporarily save the client information
CLIENT_INFO: dict = {}

def connector_callback(view,
                       set_route:str=None,
                       allowed_route:str=None,
                       callback_data:str=None,
                       **kwargs) -> None:
    """
    connector_callback:
    mapper function between route and callback view.

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
    return None


def connector_command(view,
                      commands:list=["start"],
                      set_route:str=None,
                      allowed_route:str=None,
                      **kwargs) -> None:
    """
    connector_command:
    mapper function between route and command view.

    :param view:
    :param commands:
    :param set_route:
    :param allowed_route:
    :param kwargs:
    :return:
    """


    if set_route is None:
        raise ValueError("you have to assign 'set_route' to use 'command_connector'")

    bot.message_handler(commands=commands,
                        func=lambda message: route_process(reply=message,
                                                           set_route=set_route,
                                                           allowed_route=allowed_route),
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(view)
    return None


def connector_message(view,
                      set_route:str=None,
                      allowed_route:str=None,
                      **kwargs) -> None:
    """
    connector_message:
    mapper function between route and message view.

    :param view:
    :param set_route:
    :param allowed_route:
    :param kwargs:
    :return: None
    """
    bot.message_handler(func=lambda message: route_process(reply=message,
                                                           set_route=set_route,
                                                           allowed_route=allowed_route),
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(view)
    return None


def __assign_route(client_info:dict, chat_id:int, set_route:str) -> None:
    """
    __assign_route:
    this method is charge of assigning route to telebot processes.
    this class is not designed for direct use.

    :param client_info: get from route_process
    :param chat_id: get from route_process
    :param set_route: get from route_process
    :return: None
    """

    if client_info is None:
        CLIENT_INFO.update({chat_id: {"route": "", "info": {}, "data": {}}})

    if set_route is not None:
        CLIENT_INFO[chat_id].update({"route": set_route})
    return None


def __check_callback(reply, callback_data:str) -> bool:
    """
    __check_callback:
    this method is charge of checking callback data during callback processes.
    this class is not designed for direct use.

    :param reply: get from route_process (message or callback)
    :param callback_data: get from route_process
    :return: bool
    """
    return reply.data == callback_data if callback_data is not None else True


def __check_route(client_info:dict, allowed_route:str) -> bool:
    """
    __check_route:
    this method is charge of checking allowed route during executing telebot processes.
    this class is not designed for direct use.

    :param client_info: get from route_process
    :param allowed_route: get from route_process
    :return: bool
    """

    client_route: str | None = client_info.get("route", None) if client_info is not None else None
    return client_route == allowed_route if allowed_route is not None else True


def route_process(reply,
                  set_route:str =None,
                  allowed_route:str=None,
                  callback_data:str=None,) -> bool:
    """
    route_process:
    route_process is related with validating callback data or route and assigning route for telebot processes.
    this function is return bool so that acts as a condition in handlers.

    please refer to:
    https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.message_handler

    :param reply: message or
    :param set_route:
    :param allowed_route:
    :param callback_data:
    :return:
    """

    chat_id: int = reply.from_user.id
    client_info: dict | None = CLIENT_INFO.get(chat_id, None)
    condition1: bool = __check_route(client_info=client_info, allowed_route=allowed_route)
    condition2: bool = __check_callback(reply=reply, callback_data=callback_data)

    if condition1 and condition2:
        if set_route is not None:
            __assign_route(client_info=client_info, chat_id=chat_id, set_route=set_route)
        return True

    return False
