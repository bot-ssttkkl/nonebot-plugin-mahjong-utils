import re

from nonebot import on_regex, on_command
from nonebot.params import CommandArg, RegexGroup
from ssttkkl_nonebot_utils.errors.errors import BadRequestError
from ssttkkl_nonebot_utils.interceptor.handle_error import handle_error
from mahjong_utils.point_by_han_hu import (
    get_child_point_by_han_hu,
    get_parent_point_by_han_hu,
)

from ..config import conf
from ..mapper import send_point_by_han_hu
from ..ac import command_service, sniffer_service

han_hu_pattern = r"^([1-9][0-9]*)番([1-9][0-9]*)符$"


async def handle_msg_for_han_hu(han: int, hu: int):
    try:
        parent_point = get_parent_point_by_han_hu(han, hu)
        child_point = get_child_point_by_han_hu(han, hu)
    except ValueError:
        raise BadRequestError("请输入正确的番符数目")

    await send_point_by_han_hu(han, hu, parent_point, child_point)


if conf.mahjong_utils_sniff_mode:
    han_hu_sniffer_matcher = on_regex(han_hu_pattern)
    sniffer_service.patch_matcher(han_hu_sniffer_matcher)

    @han_hu_sniffer_matcher.handle()
    @handle_error()
    async def handle(matched_groups=RegexGroup()):
        han, hu = matched_groups
        han = int(han)
        hu = int(hu)
        await handle_msg_for_han_hu(han, hu)


if conf.mahjong_utils_command_mode:
    han_hu_command_matcher = on_command("日麻番符算点", aliases={"番符"})
    command_service.patch_matcher(han_hu_command_matcher)

    @han_hu_command_matcher.handle()
    @handle_error()
    async def handle(cmd_body=CommandArg()):
        cmd_body: str = cmd_body.extract_plain_text().strip()

        try:
            han, hu = re.match(han_hu_pattern, cmd_body).groups()
            han = int(han)
            hu = int(hu)
        except Exception as e:
            raise BadRequestError("请输入正确的番符数目") from e

        await handle_msg_for_han_hu(han, hu)
