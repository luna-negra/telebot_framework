from functools import partial
from execute import (bot,
                     logger)
from core.config import ALLOWED_CHAT_TYPE


# temporarily save the client information
CLIENT_INFO: dict = {}


def connector_callback(view,
                       callback_data:str=None,
                       route:str=None,
                       allowed_pre_route:str=None,
                       **kwargs) -> None:
    """
    connector_callback:
    mapper function between route and callback view.

    :param view: function class that you want to map with specific route
    :param route: assign route to view function
    :param allowed_pre_route: route that the client can access.
    :param callback_data: set the callback data to response with InlineKeyboardButton
    :param kwargs:
    :return:
    """

    bot.callback_query_handler(func=lambda callback: route_process(reply=callback,
                                                                   allowed_pre_route=allowed_pre_route,
                                                                   callback_data=callback_data,),
                               **kwargs)(partial(view, route=route))
    return None


def connector_command(view,
                      commands:list=["start"],
                      route:str=None,
                      allowed_pre_route:str=None,
                      **kwargs) -> None:
    """
    connector_command:
    mapper function between route and command view.

    :param view:
    :param commands:
    :param route:
    :param allowed_pre_route:
    :param kwargs:
    :return:
    """


    if route is None:
        raise ValueError("you have to assign 'route' to use 'command_connector'")

    bot.message_handler(commands=commands,
                        func=lambda message: route_process(reply=message,
                                                           allowed_pre_route=allowed_pre_route),
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(partial(view, route=route))
    return None


def connector_message(view,
                      route:str=None,
                      allowed_pre_route:str=None,
                      **kwargs) -> None:
    """
    connector_message:
    mapper function between route and message view.

    :param view:
    :param route:
    :param allowed_pre_route:
    :param kwargs:
    :return: None
    """
    bot.message_handler(func=lambda message: route_process(reply=message,
                                                           allowed_pre_route=allowed_pre_route),
                        chat_types=ALLOWED_CHAT_TYPE,
                        **kwargs)(partial(view, route=route))
    return None


def __check_client_info(chat_id:int) -> dict:
    """
    __check_client_info:
    this method is charge of checking and assigning client info for first access.
    Client needs client information dictionary before using telegram bot.

    :param chat_id: get from route_process
    :return: None
    """

    if CLIENT_INFO.get(chat_id, None) is None:
        CLIENT_INFO.update({chat_id: {"route": "", "info": {}, "data": {}, "is_signin": False}})
    return CLIENT_INFO[chat_id]


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


def __check_route(client_info:dict, allowed_pre_route:str) -> bool:
    """
    __check_route:
    this method is charge of checking allowed route during executing telebot processes.
    this class is not designed for direct use.

    :param client_info: get from route_process
    :param allowed_pre_route: get from route_process
    :return: bool
    """

    client_route: str | None = client_info.get("route", None) if client_info is not None else None
    return client_route == allowed_pre_route if allowed_pre_route is not None else True


def route_process(reply,
                  allowed_pre_route:str=None,
                  callback_data:str=None,) -> bool:
    """
    route_process:
    route_process is related with validating callback data or route and assigning route for telebot processes.
    this function is return bool so that acts as a condition in handlers.

    please refer to:
    https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.message_handler

    :param reply: message or callback
    :param allowed_pre_route:
    :param callback_data:
    :return:
    """

    chat_id: int = reply.from_user.id
    client_info: dict | None = __check_client_info(chat_id=chat_id)
    condition1: bool = __check_route(client_info=client_info, allowed_pre_route=allowed_pre_route)
    condition2: bool = __check_callback(reply=reply, callback_data=callback_data)
    return True if condition1 and condition2 else False
