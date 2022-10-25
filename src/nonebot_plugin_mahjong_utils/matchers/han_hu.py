from io import StringIO

from mahjong_utils.point_by_han_hu import get_parent_point_by_han_hu, get_child_point_by_han_hu
from nonebot import on_regex, Bot
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher
from nonebot.typing import T_State

from nonebot_plugin_mahjong_utils.errors import BadRequestError
from nonebot_plugin_mahjong_utils.interceptors.handle_error import handle_error
from nonebot_plugin_mahjong_utils.utils.mapper import map_han_hu

han_hu_matcher = on_regex(r"^([1-9][0-9]*)番([1-9][0-9]*)符$")


@han_hu_matcher.handle()
@handle_error(han_hu_matcher)
async def handle(bot: Bot, event: Event, state: T_State, matcher: Matcher):
    han, hu = state["_matched_groups"]
    han = int(han)
    hu = int(hu)

    try:
        parent_point = get_parent_point_by_han_hu(han, hu)
        child_point = get_child_point_by_han_hu(han, hu)
    except ValueError:
        raise BadRequestError("请输入正确的番符数目")

    with StringIO() as sio:
        map_han_hu(sio, parent_point, child_point)

        msg = sio.getvalue()
        await matcher.send(msg)
