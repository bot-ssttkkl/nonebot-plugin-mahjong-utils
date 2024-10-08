from mahjong_utils.point_by_han_hu import get_parent_point_by_han_hu, get_child_point_by_han_hu
from nonebot import on_regex
from nonebot.params import RegexGroup
from ssttkkl_nonebot_utils.errors.errors import BadRequestError
from ssttkkl_nonebot_utils.interceptor.handle_error import handle_error

from ..mapper import send_point_by_han_hu

han_hu_matcher = on_regex(r"^([1-9][0-9]*)番([1-9][0-9]*)符$")


@han_hu_matcher.handle()
@handle_error()
async def handle(matched_groups=RegexGroup()):
    han, hu = matched_groups
    han = int(han)
    hu = int(hu)

    try:
        parent_point = get_parent_point_by_han_hu(han, hu)
        child_point = get_child_point_by_han_hu(han, hu)
    except ValueError:
        raise BadRequestError("请输入正确的番符数目")

    await send_point_by_han_hu(han, hu, parent_point, child_point)
