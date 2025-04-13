from nonebot import logger
from ssttkkl_nonebot_utils.errors.errors import BadRequestError
from mahjong_detector import detect_tiles
from mahjong_utils.models.tile import Tile
from ssttkkl_nonebot_utils.interceptor.handle_error import handle_error
from ssttkkl_nonebot_utils.interceptor.with_handling_reaction import (
    with_handling_reaction,
)
from nonebot_plugin_alconna import (
    Args,
    Image,
    Alconna,
    Arparma,
    AlconnaMatches,
    on_alconna,
)

from ..config import conf
from .pairi import handle_pairi
from ..ac import command_service

character_tile_mapping = {"tou": "1z", "nan": "2z", "sha": "3z", "pe": "4z", "haku": "5z", "hatsu": "6z", "chun": "7z"}

if conf.mahjong_utils_command_mode:
    tiles_img_analyse_command_matcher = on_alconna(Alconna("日麻手牌分析", Args["tiles", Image]), aliases={"牌理"})
    command_service.patch_matcher(tiles_img_analyse_command_matcher)

    @tiles_img_analyse_command_matcher.handle()
    @handle_error()
    @with_handling_reaction()
    async def _(result: Arparma = AlconnaMatches()):
        img = result.query[Image]("tiles")
        tiles = await detect_tiles(img)
        tiles = [character_tile_mapping.get(t, t) for t in tiles]
        tiles = [Tile.by_text(t) for t in tiles]

        logger.debug(f"tiles detect result: {tiles}")

        if tiles:
            await handle_pairi(tiles, [])
        else:
            raise BadRequestError("未识别到麻将牌")
