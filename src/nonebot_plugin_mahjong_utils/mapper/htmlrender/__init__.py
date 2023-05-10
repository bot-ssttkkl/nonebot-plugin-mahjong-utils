from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Any

from mahjong_utils.hora import Hora, RegularHoraHandPattern
from mahjong_utils.models.furo import Furo
from mahjong_utils.models.tile import Tile
from mahjong_utils.shanten import CommonShantenResult, FuroChanceShantenResult
from nonebot import require

from nonebot_plugin_mahjong_utils.mapper.plaintext.general import yaku_mapping
from nonebot_plugin_mahjong_utils.mapper.plaintext.point_by_han_hu import get_ron_text, get_tsumo_text

try:
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import template_to_pic

    require("nonebot_plugin_saa")
    from nonebot_plugin_saa import MessageFactory, Image
except Exception as e:
    raise Exception("请安装 nonebot-plugin-mahjong-utils[htmlrender]") from e

template_path = str(Path(__file__).parent / "templates")


async def _render(template_name: str, templates: Dict[str, Any]) -> MessageFactory:
    pic = await template_to_pic(
        template_path=template_path,
        template_name=template_name,
        templates=templates,
        pages={
            "base_url": f"file://{template_path}",
            "viewport": {"width": 800, "height": 10}
        }
    )
    return MessageFactory([Image(pic)])


def convert_improvement_view(improvement):
    imp = []

    for t in improvement:
        imp.append({
            "tile": t,
            "discard": [x.discard for x in improvement[t]],
            "advance_num": improvement[t][0].advance_num
        })

    imp.sort(key=lambda x: x["tile"])

    return imp


async def render_common_shanten_result(result: CommonShantenResult, tiles: List[Tile]) -> MessageFactory:
    templates = {
        "tiles": tiles,
        "result": result,
        "convert_improvement_view": convert_improvement_view
    }

    if not result.with_got:
        template_name = "shanten_without_got.html"
        if result.improvement is not None:
            improvement = []

            for t in result.improvement:
                imp = {
                    "tile": t,
                    "discard": [x.discard for x in result.improvement[t]],
                    "advance_num": result.improvement[t][0].advance_num
                }
                improvement.append(imp)

            improvement.sort(key=lambda x: x["tile"])

            templates['improvement'] = improvement
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


async def render_furo_chance_shanten_result(result: FuroChanceShantenResult, tiles: List[Tile], chance_tile: Tile,
                                            tile_from: int) -> MessageFactory:
    templates = {
        "tiles": tiles,
        "chance_tile": chance_tile,
        "tile_from": tile_from,
        "result": result,
        "convert_improvement_view": convert_improvement_view
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


async def render_hora(hora_ron: Hora, hora_tsumo: Hora, tiles: List[Tile], furo: List[Furo]) -> MessageFactory:
    templates = {
        "tiles": tiles,
        "furo": furo,
        "regular": isinstance(hora_ron.pattern, RegularHoraHandPattern),
        "pattern": hora_ron.pattern,
        "hora_ron": hora_ron,
        "hora_tsumo": hora_tsumo,
        "yaku_mapping": yaku_mapping,
        "get_ron_text": get_ron_text,
        "get_tsumo_text": get_tsumo_text
    }
    template_name = "hora.html"
    return await _render(template_name, templates)
