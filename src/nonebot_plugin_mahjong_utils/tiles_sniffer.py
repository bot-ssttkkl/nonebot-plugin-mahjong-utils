import re
from io import StringIO

from mahjong_utils.hora import build_hora
from mahjong_utils.models.furo import parse_furo
from mahjong_utils.models.tile import parse_tiles
from mahjong_utils.shanten import calc_shanten, calc_shanten_with_got_tile
from nonebot import on_regex, Bot
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher
from nonebot.typing import T_State

from nonebot_plugin_mahjong_utils.handle_error import handle_error
from nonebot_plugin_mahjong_utils.mapper import map_shanten_result, map_shanten_with_got_tile_result, map_hora
from nonebot_plugin_mahjong_utils.parser import parse_wind, try_parse_extra_yaku

tiles_pattern = r"([0-9]+(m|p|s|z){1})+"
furo_pattern = r"[0-9]+(m|p|s|z){1}"

tiles_matcher = on_regex(rf"^{tiles_pattern}(\s{furo_pattern})*")


@tiles_matcher.handle()
@handle_error(tiles_matcher)
async def sniffer(bot: Bot, event: Event, state: T_State, matcher: Matcher):
    text = event.get_plaintext().split(' ')

    tiles = parse_tiles(text[0])
    furo = []
    tsumo = False
    dora = 0
    self_wind = None
    round_wind = None
    extra_yaku = set()

    for t in text[1:]:
        if re.match(furo_pattern, t):
            furo.append(parse_furo(t))
        elif t == "自摸":
            tsumo = True
        elif t.startswith("dora"):
            dora = int(t[len("dora"):])
        elif t.startswith("自风"):
            self_wind = parse_wind(t[len("自风"):])
        elif t.startswith("场风"):
            round_wind = parse_wind(t[len("场风"):])
        else:
            yaku = try_parse_extra_yaku(t)
            if yaku is not None:
                extra_yaku.add(yaku)

    if len(tiles) % 3 == 1:
        result = calc_shanten(tiles, furo)
        with StringIO() as sio:
            map_shanten_result(sio, result)
            msg = sio.getvalue().strip()

        await matcher.send(msg)
    elif len(tiles) % 3 == 2:
        result = calc_shanten_with_got_tile(tiles, furo)
        if result.shanten == -1:
            # 分析和牌
            hora = build_hora(tiles[:-1], furo, tiles[-1], tsumo,
                              dora=dora, self_wind=self_wind, round_wind=round_wind,
                              extra_yaku=extra_yaku)
            with StringIO() as sio:
                map_hora(sio, hora)
                msg = sio.getvalue().strip()
        else:
            with StringIO() as sio:
                map_shanten_with_got_tile_result(sio, result)
                msg = sio.getvalue().strip()

        await matcher.send(msg)
