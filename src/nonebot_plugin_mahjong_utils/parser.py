from typing import Optional

from mahjong_utils.models.wind import Wind
from mahjong_utils.yaku import Yaku
from mahjong_utils.yaku.extra import *


def try_parse_wind(text: str) -> Optional[Wind]:
    if text == "东":
        return Wind.east
    if text == "南":
        return Wind.south
    if text == "西":
        return Wind.west
    if text == "北":
        return Wind.north
    return None


extra_yaku_reversed_mapping = {
    "立直": richi,
    "一发": ippatsu,
    "岭上开花": rinshan,
    "岭上": rinshan,
    "枪杠": chankan,
    "海底": haitei,
    "海底捞月": haitei,
    "河底": houtei,
    "河底捞鱼": houtei,
    "两立直": w_richi,
    "天和": tenhou,
    "地和": chihou,
}


def try_parse_extra_yaku(text: str) -> Optional[Yaku]:
    return extra_yaku_reversed_mapping.get(text, None)
