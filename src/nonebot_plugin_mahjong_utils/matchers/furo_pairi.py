from io import StringIO
from typing import Sequence

from nonebot import logger, on_regex
from nonebot.internal.adapter import Event
from mahjong_utils.shanten import furo_chance_shanten
from mahjong_utils.models.tile import Tile, parse_tiles
from ssttkkl_nonebot_utils.errors.errors import BadRequestError
from ssttkkl_nonebot_utils.interceptor.handle_error import handle_error
from ssttkkl_nonebot_utils.interceptor.with_handling_reaction import (
    with_handling_reaction,
)

from ..config import conf
from ..ac import sniffer_service
from ..utils.executor import run_in_my_executor
from ..mapper import send_furo_chance_shanten_result
from ..mapper.plaintext.shanten import map_furo_chance_shanten_result

tiles_pattern = r"([0-9]+(m|p|s|z){1})+"
chance_tile_pattern = r"([0-9](m|p|s|z){1})"
furo_pairi_pattern = rf"^{tiles_pattern}(\^|\<|\>){chance_tile_pattern}$"


def to_msg(tiles: Sequence[Tile], chance_tile: Tile, tile_from: int):
    result = furo_chance_shanten(tiles, chance_tile, tile_from == 3)
    with StringIO() as sio:
        map_furo_chance_shanten_result(sio, result, tiles, chance_tile, tile_from)

        msg = sio.getvalue().strip()
        return msg


async def handle_msg_for_furo_pairi(text: str):
    logger.debug(f"furo_pairi: {text}")
    if ">" in text:
        tiles, chance_tile = text.split(">")
        tile_from = 1
    elif "^" in text:
        tiles, chance_tile = text.split("^")
        tile_from = 2
    elif "<" in text:
        tiles, chance_tile = text.split("<")
        tile_from = 3
    else:
        raise BadRequestError(f"invalid format: {text}")

    tiles = parse_tiles(tiles)
    chance_tile = Tile.by_text(chance_tile)

    if len(tiles) % 3 == 0:
        raise BadRequestError(f"invalid length of hand: {len(tiles)}")

    result = await run_in_my_executor(
        furo_chance_shanten, tiles, chance_tile, tile_from == 3
    )
    await send_furo_chance_shanten_result(result, tiles, chance_tile, tile_from)


if conf.mahjong_utils_sniff_mode:
    furo_judge_sniffer = on_regex(furo_pairi_pattern)
    sniffer_service.patch_matcher(furo_judge_sniffer)

    @furo_judge_sniffer.handle()
    @handle_error(silently=True)
    @with_handling_reaction()
    async def handle(event: Event):
        text = event.get_plaintext().strip()
        await handle_msg_for_furo_pairi(text)
