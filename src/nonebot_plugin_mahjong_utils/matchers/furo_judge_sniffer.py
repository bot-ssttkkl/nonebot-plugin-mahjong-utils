from io import StringIO
from typing import Sequence

from mahjong_utils.models.tile import parse_tiles, Tile
from mahjong_utils.shanten import furo_chance_shanten
from nonebot import on_regex
from nonebot.internal.adapter import Event
from ssttkkl_nonebot_utils.errors.errors import BadRequestError
from ssttkkl_nonebot_utils.interceptor.handle_error import handle_error
from ssttkkl_nonebot_utils.interceptor.with_handling_reaction import with_handling_reaction

from ..mapper import send_furo_chance_shanten_result
from ..mapper.plaintext.shanten import map_furo_chance_shanten_result
from ..utils.executor import run_in_my_executor

tiles_pattern = r"([0-9]+(m|p|s|z){1})+"
chance_tile_pattern = r"([0-9](m|p|s|z){1})"

furo_judge_sniffer = on_regex(rf"^{tiles_pattern}(\^|\<|\>){chance_tile_pattern}$")


def to_msg(tiles: Sequence[Tile], chance_tile: Tile, tile_from: int):
    result = furo_chance_shanten(tiles, chance_tile, tile_from == 3)
    with StringIO() as sio:
        map_furo_chance_shanten_result(sio, result, tiles, chance_tile, tile_from)

        msg = sio.getvalue().strip()
        return msg


@furo_judge_sniffer.handle()
@handle_error(silently=True)
@with_handling_reaction()
async def handle(event: Event):
    text = event.get_plaintext()
    if '>' in text:
        tiles, chance_tile = event.get_plaintext().split('>')
        tile_from = 1
    elif '^' in text:
        tiles, chance_tile = event.get_plaintext().split('^')
        tile_from = 2
    elif '<' in text:
        tiles, chance_tile = event.get_plaintext().split('<')
        tile_from = 3
    else:
        return

    tiles = parse_tiles(tiles)
    chance_tile = Tile.by_text(chance_tile)

    if len(tiles) % 3 == 0:
        raise BadRequestError(f"invalid length of hand: {len(tiles)}")

    result = await run_in_my_executor(furo_chance_shanten, tiles, chance_tile, tile_from == 3)
    await send_furo_chance_shanten_result(result, tiles, chance_tile, tile_from)
