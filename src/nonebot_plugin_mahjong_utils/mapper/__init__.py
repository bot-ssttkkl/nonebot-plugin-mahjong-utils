from io import StringIO
from typing import List, Optional

from mahjong_utils.hora import Hora
from mahjong_utils.models.furo import Furo
from mahjong_utils.models.tile import Tile
from mahjong_utils.point_by_han_hu import ParentPoint, ChildPoint
from mahjong_utils.shanten import CommonShantenResult, FuroChanceShantenResult
from nonebot_plugin_saa import Text, MessageFactory

from .plaintext.point_by_han_hu import map_point_by_han_hu
from ..config import conf

if conf.mahjong_utils_send_image:
    from .htmlrender import render_common_shanten_result, render_furo_chance_shanten_result, render_hora


    async def send_common_shanten_result(result: CommonShantenResult, tiles: List[Tile]):
        await (await render_common_shanten_result(result, tiles)).send()


    async def send_furo_chance_shanten_result(result: FuroChanceShantenResult, tiles: List[Tile], chance_tile: Tile,
                                              tile_from: int):
        await (await render_furo_chance_shanten_result(result, tiles, chance_tile, tile_from)).send()


    async def send_hora(hora_ron: Hora, hora_tsumo: Hora, tiles: List[Tile], furo: List[Furo]):
        await (await render_hora(hora_ron, hora_tsumo, tiles, furo)).send()
else:

    from .plaintext.hora import map_hora
    from .plaintext.shanten import map_common_shanten_result, map_furo_chance_shanten_result


    async def send_common_shanten_result(result: CommonShantenResult, tiles: List[Tile]):
        with StringIO() as sio:
            map_common_shanten_result(sio, result, tiles)
            await MessageFactory(Text(sio.getvalue())).send(reply=True)


    async def send_furo_chance_shanten_result(result: FuroChanceShantenResult, tiles: List[Tile], chance_tile: Tile,
                                              tile_from: int):
        with StringIO() as sio:
            map_furo_chance_shanten_result(sio, result, tiles, chance_tile, tile_from)
            await MessageFactory(Text(sio.getvalue())).send(reply=True)


    async def send_hora(hora_ron: Hora, hora_tsumo: Hora, tiles: List[Tile], furo: List[Furo]):
        with StringIO() as sio:
            map_hora(sio, hora_ron, hora_tsumo, tiles, furo)
            await MessageFactory(Text(sio.getvalue())).send(reply=True)


async def send_point_by_han_hu(parent_point: Optional[ParentPoint],
                               child_point: Optional[ChildPoint]):
    with StringIO() as sio:
        map_point_by_han_hu(sio, parent_point, child_point)
        await MessageFactory(Text(sio.getvalue())).send(reply=True)
