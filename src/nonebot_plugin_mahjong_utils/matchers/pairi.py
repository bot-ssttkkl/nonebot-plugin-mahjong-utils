import re
from typing import Optional

from mahjong_utils.yaku import Yaku
from nonebot import logger, on_regex
from mahjong_utils.shanten import shanten
from mahjong_utils.models.furo import Furo
from mahjong_utils.models.wind import Wind
from nonebot.internal.adapter import Event
from mahjong_utils.models.tile import Tile, parse_tiles
from mahjong_utils.hora import build_hora_from_shanten_result
from ssttkkl_nonebot_utils.errors.errors import BadRequestError
from ssttkkl_nonebot_utils.interceptor.handle_error import handle_error
from ssttkkl_nonebot_utils.interceptor.with_handling_reaction import (
    with_handling_reaction,
)

from ..config import conf
from ..ac import sniffer_service
from ..utils.executor import run_in_my_executor
from ..mapper import send_hora, send_common_shanten_result
from ..utils.parser import try_parse_wind, try_parse_extra_yaku

tiles_pattern = r"([0-9]+(m|p|s|z){1})+"
furo_pattern = r"[0-9]+(m|p|s|z){1}"
pairi_pattern = rf"^{tiles_pattern}(\s{furo_pattern})*(\s.*)*$"


async def handle_msg_for_pairi(text: str):
    logger.debug(f"pairi: {text}")

    text = text.split(" ")
    tiles = parse_tiles(text[0])
    furo = []
    dora = 0
    self_wind = None
    round_wind = None
    extra_yaku = set()

    for t in text[1:]:
        if re.match(furo_pattern, t):
            furo.append(Furo.parse(t))
        elif len(t) > 4 and t[:4].lower() == "dora":
            dora = int(t[len("dora") :])
        elif t.startswith("自风"):
            if self_wind is None:
                self_wind = try_parse_wind(t[len("自风") :])
        elif t.endswith("家"):
            if self_wind is None:
                self_wind = try_parse_wind(t[: len("家")])
        elif t.startswith("场风"):
            if round_wind is None:
                round_wind = try_parse_wind(t[len("场风") :])
        else:
            yaku = try_parse_extra_yaku(t)
            if yaku is not None:
                extra_yaku.add(yaku)

    await handle_pairi(
        tiles,
        furo,
        dora=dora,
        self_wind=self_wind,
        round_wind=round_wind,
        extra_yaku=extra_yaku,
        ignore_short_hand=True,
    )


async def handle_pairi(
    tiles: list[Tile],
    furo: list[Furo],
    *,
    dora: int = 0,
    self_wind: Optional[Wind] = None,
    round_wind: Optional[Wind] = None,
    extra_yaku: Optional[set[Yaku]] = None,
    ignore_short_hand: bool = False,
):
    if len(tiles) % 3 == 0:
        raise BadRequestError("手牌数量不合法")

    if len(tiles) % 3 == 2:
        got = tiles[-1]
    else:
        got = None

    if ignore_short_hand and len(furo) == 0 and len(tiles) < 3:
        # 少于三张牌不进行计算
        return

    tiles = [Tile.by_type_and_num(x.tile_type, x.real_num) for x in tiles]
    if got is not None:
        got = Tile.by_type_and_num(got.tile_type, got.real_num)

    result = await run_in_my_executor(shanten, tiles, furo)
    if result.shanten == -1 and len(result.hand.furo) * 3 + len(tiles) == 14:
        # 分析和牌
        hora_ron = await run_in_my_executor(
            build_hora_from_shanten_result,
            result,
            got,
            False,
            dora=dora,
            self_wind=self_wind,
            round_wind=round_wind,
            extra_yaku=extra_yaku,
        )
        hora_tsumo = await run_in_my_executor(
            build_hora_from_shanten_result,
            result,
            got,
            True,
            dora=dora,
            self_wind=self_wind,
            round_wind=round_wind,
            extra_yaku=extra_yaku,
        )
        await send_hora(hora_ron, hora_tsumo, tiles, furo)
    else:
        await send_common_shanten_result(result, tiles)


tiles_sniffer = on_regex(pairi_pattern)
sniffer_service.patch_matcher(tiles_sniffer)


if conf.mahjong_utils_sniff_mode:

    @tiles_sniffer.handle()
    @handle_error(silently=True)
    @with_handling_reaction()
    async def handle(event: Event):
        text = event.get_plaintext().strip()
        await handle_msg_for_pairi(text)
