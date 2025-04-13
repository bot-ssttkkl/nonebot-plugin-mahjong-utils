import re

from nonebot import on_command
from nonebot.params import CommandArg
from ssttkkl_nonebot_utils.errors.errors import BadRequestError
from ssttkkl_nonebot_utils.interceptor.handle_error import handle_error
from ssttkkl_nonebot_utils.interceptor.with_handling_reaction import (
    with_handling_reaction,
)

from ..config import conf
from ..ac import command_service
from .pairi import pairi_pattern, handle_msg_for_pairi
from .furo_pairi import furo_pairi_pattern, handle_msg_for_furo_pairi

if conf.mahjong_utils_command_mode:
    tiles_analyse_command_matcher = on_command(
        "日麻手牌分析", aliases={"牌理"}, priority=10
    )
    command_service.patch_matcher(tiles_analyse_command_matcher)

    @tiles_analyse_command_matcher.handle()
    @handle_error()
    @with_handling_reaction()
    async def handle(cmd_body=CommandArg()):
        cmd_body: str = cmd_body.extract_plain_text().strip()

        furo_pairi_match = re.match(furo_pairi_pattern, cmd_body)
        if furo_pairi_match is not None:
            await handle_msg_for_furo_pairi(cmd_body)
            return

        pairi_match = re.match(pairi_pattern, cmd_body)
        if pairi_match is not None:
            await handle_msg_for_pairi(cmd_body)
            return

        raise BadRequestError("请输入正确的牌型")
