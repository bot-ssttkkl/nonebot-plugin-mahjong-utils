from io import BytesIO

from nonebot import logger
from mahjong_utils.models.tile import Tile
from ssttkkl_nonebot_utils.errors.errors import BadRequestError
from ssttkkl_nonebot_utils.interceptor.handle_error import handle_error
from ssttkkl_nonebot_utils.interceptor.with_handling_reaction import (
    with_handling_reaction,
)
from nonebot_plugin_alconna import (
    Args,
    Image,
    Match,
    Alconna,
    AlconnaMatch,
    on_alconna,
    image_fetch,
)

from nonebot_plugin_mahjong_utils.utils.executor import run_in_my_executor

from ..config import conf
from .pairi import handle_pairi
from ..ac import command_service

try:
    from mahjong_detector import detect_tiles

    MAHJONG_DETECTOR_AVAILABLE = True
except:
    MAHJONG_DETECTOR_AVAILABLE = False

character_tile_mapping = {
    "tou": "1z",
    "nan": "2z",
    "sha": "3z",
    "pe": "4z",
    "haku": "5z",
    "hatsu": "6z",
    "chun": "7z",
}

if MAHJONG_DETECTOR_AVAILABLE and conf.mahjong_utils_command_mode:
    tiles_img_analyse_command_matcher = on_alconna(
        Alconna("日麻手牌分析", Args["img", Image]),
        aliases={"牌理"},
        use_cmd_start=True,
        priority=1,
        block=True,
    )
    command_service.patch_matcher(tiles_img_analyse_command_matcher)

    @tiles_img_analyse_command_matcher.handle()
    @handle_error()
    @with_handling_reaction()
    async def _(img: Match[bytes] = AlconnaMatch("img", image_fetch)):
        tiles = await run_in_my_executor(detect_tiles, BytesIO(img.result))
        tiles = [character_tile_mapping.get(t, t) for t in tiles]
        tiles = [Tile.by_text(t) for t in tiles]

        logger.debug(f"tiles detect result: {tiles}")

        if tiles:
            try:
                await handle_pairi(tiles, [])
            except BadRequestError as e:
                raise BadRequestError(f"{e.message}，从图片检测到的手牌为{tiles}")
        else:
            raise BadRequestError("未识别到麻将牌")
