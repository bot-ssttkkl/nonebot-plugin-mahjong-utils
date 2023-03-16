from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Any

from mahjong_utils.hora import Hora, RegularHoraHandPattern
from mahjong_utils.models.furo import Furo
from mahjong_utils.models.tile import Tile
from mahjong_utils.shanten import CommonShantenResult, FuroChanceShantenResult
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot_plugin_htmlrender import template_to_pic

from nonebot_plugin_mahjong_utils.mapper.general import yaku_mapping

template_path = str(Path(__file__).parent / "templates")


async def _render(template_name: str, templates: Dict[str, Any]):
    pic = await template_to_pic(
        template_path=template_path,
        template_name=template_name,
        templates=templates,
        pages={
            "base_url": f"file://{template_path}",
            "viewport": {"width": 800, "height": 10}
        }
    )
    return Message([MessageSegment.image(pic)])


async def render_shanten(result: CommonShantenResult, tiles: List[Tile]) -> Message:
    templates = {
        "tiles": tiles,
        "result": result
    }

    if not result.with_got:
        template_name = "shanten_without_got.html"
    else:
        template_name = "shanten_with_got.html"

        grouped_shanten = defaultdict(dict)
        for discard, shanten_after_discard in result.discard_to_advance.items():
            grouped_shanten[shanten_after_discard.shanten][("discard", discard)] = shanten_after_discard
        for ankan, ankan_after_discard in result.ankan_to_advance.items():
            grouped_shanten[ankan_after_discard.shanten][("ankan", ankan)] = ankan_after_discard
        grouped_shanten = list(sorted(grouped_shanten.items()))

        for i, (key, value) in enumerate(grouped_shanten):
            grouped_shanten[i] = key, sorted(value.items(), key=lambda x: x[1].advance_num, reverse=True)

        templates['grouped_shanten'] = grouped_shanten

    return await _render(template_name, templates)


async def render_furo_chance(result: FuroChanceShantenResult, tiles: List[Tile], chance_tile: Tile,
                             tile_from: int) -> Message:
    templates = {
        "tiles": tiles,
        "chance_tile": chance_tile,
        "tile_from": tile_from,
        "result": result
    }
    template_name = "shanten_with_furo_chance.html"

    grouped_shanten = defaultdict(dict)

    shanten_info = result.shanten_info

    if shanten_info.pass_ is not None:
        grouped_shanten[shanten_info.pass_.shanten][("pass",)] = shanten_info.pass_

    if shanten_info.pon is not None:
        for discard, shanten_after_pon_discard in shanten_info.pon.discard_to_advance.items():
            grouped_shanten[shanten_after_pon_discard.shanten][("pon", discard)] = shanten_after_pon_discard

    if shanten_info.minkan is not None:
        grouped_shanten[shanten_info.minkan.shanten][("minkan",)] = shanten_info.minkan

    for tatsu, shanten_after_chi in shanten_info.chi.items():
        for discard, shanten_after_chi_discard in shanten_after_chi.discard_to_advance.items():
            grouped_shanten[shanten_after_chi_discard.shanten][("chi", tatsu, discard)] = shanten_after_chi_discard

    grouped_shanten = list(sorted(grouped_shanten.items()))

    for i, (key, value) in enumerate(grouped_shanten):
        grouped_shanten[i] = key, sorted(value.items(), key=lambda x: x[1].advance_num, reverse=True)

    templates['grouped_shanten'] = grouped_shanten

    return await _render(template_name, templates)


async def render_hora(hora_ron: Hora, hora_tsumo: Hora, tiles: List[Tile], furo: List[Furo]) -> Message:
    templates = {
        "tiles": tiles,
        "furo": furo,
        "regular": isinstance(hora_ron.pattern, RegularHoraHandPattern),
        "pattern": hora_ron.pattern,
        "hora_ron": hora_ron,
        "hora_tsumo": hora_tsumo,
        "yaku_mapping": yaku_mapping
    }
    template_name = "hora.html"
    return await _render(template_name, templates)