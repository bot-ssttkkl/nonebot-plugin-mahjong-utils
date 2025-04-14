from io import StringIO
from typing import List, Optional

from mahjong_utils.hora import Hora
from mahjong_utils.models.furo import Furo
from mahjong_utils.models.tile import Tile
from nonebot_plugin_saa import Text, Image, MessageFactory
from mahjong_utils.point_by_han_hu import ChildPoint, ParentPoint
from mahjong_utils.shanten import CommonShantenResult, FuroChanceShantenResult

from ..config import conf
from .sent_store import last_sent
from .plaintext.point_by_han_hu import map_point_by_han_hu


async def _send_text(text: str):
    if conf.mahjong_utils_test:
        last_sent["text"] = text
    await MessageFactory(Text(text)).send(reply=True)


async def _send_img(img: bytes):
    if conf.mahjong_utils_test:
        last_sent["img"] = img
    await MessageFactory(Image(img)).send(reply=True)


async def send_common_shanten_result(result: CommonShantenResult, tiles: List[Tile]):
    if conf.mahjong_utils_send_image:
        from .htmlrender import render_common_shanten_result

        await _send_img(await render_common_shanten_result(result, tiles))

    else:
        from .plaintext.shanten import map_common_shanten_result

        with StringIO() as sio:
            map_common_shanten_result(sio, result, tiles)
            await _send_text(sio.getvalue())


async def send_furo_chance_shanten_result(
    result: FuroChanceShantenResult,
    tiles: List[Tile],
    chance_tile: Tile,
    tile_from: int,
):
    if conf.mahjong_utils_send_image:
        from .htmlrender import render_furo_chance_shanten_result

        await _send_img(
            await render_furo_chance_shanten_result(
                result, tiles, chance_tile, tile_from
            )
        )

    else:
        from .plaintext.shanten import map_furo_chance_shanten_result

        with StringIO() as sio:
            map_furo_chance_shanten_result(sio, result, tiles, chance_tile, tile_from)
            await _send_text(sio.getvalue())


async def send_hora(
    hora_ron: Hora, hora_tsumo: Hora, tiles: List[Tile], furo: List[Furo]
):
    if conf.mahjong_utils_send_image:
        from .htmlrender import render_hora

        await _send_img(await render_hora(hora_ron, hora_tsumo, tiles, furo))

    else:
        from .plaintext.hora import map_hora

        with StringIO() as sio:
            map_hora(sio, hora_ron, hora_tsumo, tiles, furo)
            await _send_text(sio.getvalue())


async def send_point_by_han_hu(
    han: int,
    hu: int,
    parent_point: Optional[ParentPoint],
    child_point: Optional[ChildPoint],
):
    with StringIO() as sio:
        sio.write(f"{han}番{hu}符\n")
        map_point_by_han_hu(sio, parent_point, child_point)
        await _send_text(sio.getvalue())
