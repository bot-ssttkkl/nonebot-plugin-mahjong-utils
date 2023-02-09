from collections import defaultdict
from typing import TextIO, Optional, Tuple, cast

from mahjong_utils.hora import Hora
from mahjong_utils.models.hand_pattern import HandPattern, RegularHandPattern
from mahjong_utils.models.tile import tiles_text, Tile
from mahjong_utils.models.wind import Wind
from mahjong_utils.shanten import ShantenResult, ShantenWithFuroChance, ShantenWithoutGot
from mahjong_utils.yaku.common import *
from mahjong_utils.yaku.extra import *
from mahjong_utils.yaku.yakuman import *

yaku_mapping = {
    tsumo: "门清自摸",
    pinhu: "平和",
    tanyao: "断幺",
    ipe: "一杯口",
    self_wind: "自风",
    round_wind: "场风",
    haku: "白",
    hatsu: "发",
    chun: "中",
    sanshoku: "三色同顺",
    ittsu: "一气通贯",
    chanta: "混全带幺九",
    chitoi: "七对子",
    toitoi: "对对和",
    sananko: "三暗刻",
    honroto: "混老头",
    sandoko: "三色同刻",
    sankantsu: "三杠子",
    shosangen: "小三元",
    honitsu: "混一色",
    junchan: "纯全带幺九",
    ryanpe: "两杯口",
    chinitsu: "清一色",
    richi: "立直",
    ippatsu: "一发",
    rinshan: "岭上开花",
    chankan: "枪杠",
    haitei: "海底摸月",
    houtei: "河底捞鱼",
    w_richi: "两立直",
    tenhou: "天和",
    chihou: "地和",
    kokushi: "国士无双",
    suanko: "四暗刻",
    daisangen: "大三元",
    tsuiso: "字一色",
    shousushi: "小四喜",
    lyuiso: "绿一色",
    chinroto: "清老头",
    sukantsu: "四杠子",
    churen: "九莲宝灯",
    daisushi: "大四喜",
    churen_nine_waiting: "纯正九莲宝灯",
    suanko_tanki: "四暗刻单骑",
    kokushi_thirteen_waiting: "国士无双十三面"
}

num_mapping = {
    1: "一",
    2: "两",
    3: "三",
    4: "四",
    5: "五",
    6: "六"
}

wind_mapping = {
    Wind.east: "东",
    Wind.south: "南",
    Wind.west: "西",
    Wind.north: "北"
}


def map_han_hu(io: TextIO,
               parent_point: Optional[Tuple[int, int]],
               child_point: Optional[Tuple[int, int, int]]):
    if parent_point is not None:
        parent_ron, parent_tsumo = parent_point
        io.write("亲家和牌时：")
        if parent_tsumo:
            io.write("自摸")
            io.write(str(parent_tsumo * 3))
            io.write(' (')
            io.write(str(parent_tsumo))
            io.write(" ALL)")

        if parent_tsumo and parent_ron:
            io.write("，")

        if parent_ron:
            io.write("荣和")
            io.write(str(parent_ron))
        io.write("\n")

    if child_point is not None:
        child_ron, child_tsumo_parent, child_tsumo_child = child_point
        io.write("子家和牌时：")
        if child_tsumo_parent:
            io.write("自摸")
            io.write(str(child_tsumo_parent + child_tsumo_child * 2))
            io.write(' (')
            io.write(str(child_tsumo_parent))
            io.write(" ")
            io.write(str(child_tsumo_child))
            io.write(")")

        if child_tsumo_parent and child_ron:
            io.write("，")

        if child_ron:
            io.write("荣和")
            io.write(str(child_ron))
        io.write("\n")


def map_hand(io: TextIO, hand: HandPattern, *, got: Optional[Tile] = None):
    tiles = sorted(hand.tiles)

    if isinstance(hand, RegularHandPattern):
        for fr in hand.furo:
            for t in fr.tiles:
                tiles.remove(t)

    if got is not None:
        tiles.remove(got)
        tiles.append(got)

    io.write(tiles_text(tiles))
    io.write(' ')

    if isinstance(hand, RegularHandPattern):
        for fr in hand.furo:
            io.write(str(fr))
            io.write(' ')


def map_shanten_without_got(io: TextIO, shanten: ShantenWithoutGot):
    io.write("进张：")
    io.write(tiles_text(sorted(shanten.advance)))
    io.write(" (")
    io.write(str(shanten.advance_num))
    io.write("张")
    if shanten.shanten == 1:
        io.write("：好型")
        io.write(str(shanten.good_shape_advance_num))
        io.write("张，愚型")
        io.write(str(shanten.advance_num - shanten.good_shape_advance_num))
        io.write("张")
    io.write(")")


def map_shanten_result(io: TextIO, result: ShantenResult, *, got: Optional[Tile] = None):
    map_hand(io, result.hand.patterns[0], got=got)
    io.write('\n')

    if not result.with_got:
        if result.shanten == -1:
            io.write("和牌\n")
        elif result.shanten == 0:
            io.write("听牌：\n")
        else:
            io.write(str(result.shanten))
            io.write("向听：\n")

        map_shanten_without_got(io, cast(ShantenWithoutGot, result.shanten_info))
        io.write("\n")
    else:
        grouped = defaultdict(dict)

        for discard, shanten_after_discard in result.discard_to_advance.items():
            grouped[shanten_after_discard.shanten][("discard", discard)] = shanten_after_discard

        for ankan, ankan_after_discard in result.ankan_to_advance.items():
            grouped[ankan_after_discard.shanten][("ankan", ankan)] = ankan_after_discard

        records = 0
        tot_records = sum(map(lambda x: len(x), grouped.values()))

        for shanten_num in sorted(grouped.keys()):
            if result.shanten == -1:
                io.write("和牌\n")
                break
            elif shanten_num == 0:
                io.write("听牌：\n")
            else:
                io.write(str(shanten_num))
                io.write("向听")
                if shanten_num != result.shanten:
                    io.write("（退向）")
                io.write("：\n")

            ordered = sorted(grouped[shanten_num].items(), key=lambda x: x[1].advance_num, reverse=True)

            for action, shanten_after_discard in ordered:
                io.write("[")
                if action[0] == 'discard':
                    io.write(f"打{action[1]}")
                elif action[0] == 'ankan':
                    io.write(f"暗杠{action[1]}")
                io.write("]  ")

                map_shanten_without_got(io, shanten_after_discard)
                io.write("\n")

                records += 1

                if records >= 10:
                    break

            io.write("\n")

            if records >= 10:
                break

        if records < tot_records:
            io.write("（只显示最优的前10种打法）")


def map_furo_chance_shanten_result(io: TextIO, result: ShantenResult, chance_tile: Tile, tile_from: int):
    map_hand(io, result.hand.patterns[0])
    if tile_from == 1:
        io.write("下家打")
    elif tile_from == 2:
        io.write("对家打")
    elif tile_from == 3:
        io.write("上家打")
    io.write(str(chance_tile))
    io.write('\n')

    grouped = defaultdict(dict)

    shanten_info = cast(ShantenWithFuroChance, result.shanten_info)

    if shanten_info.pass_ is not None:
        grouped[shanten_info.pass_.shanten][("pass",)] = shanten_info.pass_

    if shanten_info.pon is not None:
        for discard, shanten_after_pon_discard in shanten_info.pon.discard_to_advance.items():
            grouped[shanten_after_pon_discard.shanten][("pon", discard)] = shanten_after_pon_discard

    if shanten_info.minkan is not None:
        grouped[shanten_info.minkan.shanten][("minkan",)] = shanten_info.minkan

    for tatsu, shanten_after_chi in shanten_info.chi.items():
        for discard, shanten_after_chi_discard in shanten_after_chi.discard_to_advance.items():
            grouped[shanten_after_chi_discard.shanten][("chi", tatsu, discard)] = shanten_after_chi_discard

    records = 0
    tot_records = sum(map(lambda x: len(x), grouped.values()))

    for shanten_num in sorted(grouped.keys()):
        if result.shanten == -1:
            io.write("和牌\n")
            break
        elif shanten_num == 0:
            io.write("听牌：\n")
        else:
            io.write(str(shanten_num))
            io.write("向听")
            if shanten_num != result.shanten:
                io.write("（退向）")
            io.write("：\n")

        ordered = sorted(grouped[shanten_num].items(), key=lambda x: x[1].advance_num, reverse=True)

        for action, shanten_after_action in ordered:
            io.write("[")
            if action[0] == 'pass':
                io.write("PASS")
            elif action[0] == 'chi':
                io.write(f"{action[1]}吃打{action[2]}")
            elif action[0] == 'pon':
                io.write(f"碰打{action[1]}")
            elif action[0] == 'minkan':
                io.write(f"杠")
            io.write("]  ")

            map_shanten_without_got(io, shanten_after_action)
            io.write("\n")

            records += 1

            if records >= 10:
                break

        io.write("\n")

        if records >= 10:
            break

    if records < tot_records:
        io.write("（只显示最优的前10种打法）")


def map_han_hu_text(io: TextIO, han: int, hu: int):
    io.write(str(han))
    io.write("番")
    io.write(str(hu))
    io.write("符")

    han_type = None
    if han >= 13:
        han_type = "累计役满"
    elif han >= 11:
        han_type = "三倍满"
    elif han >= 8:
        han_type = "倍满"
    elif han >= 6:
        han_type = "跳满"
    elif han >= 5 or han == 4 and hu >= 40:
        han_type = "满贯"

    if han_type is not None:
        io.write("  ")
        io.write(han_type)


def map_yakuman_text(io: TextIO, yakuman: int):
    io.write(num_mapping[yakuman])
    io.write("倍役满")


def map_hora(io: TextIO, hora_ron: Hora, hora_tsumo: Hora, *, got: Optional[Tile] = None):
    hora = hora_ron
    map_hand(io, hora.pattern, got=got)

    if hora.dora > 0:
        io.write("dora")
        io.write(str(hora.dora))
        io.write(" ")

    if hora.self_wind is not None:
        io.write("自风")
        io.write(wind_mapping[hora.self_wind])
        io.write(" ")

    if hora.round_wind is not None:
        io.write("场风")
        io.write(wind_mapping[hora.round_wind])
        io.write(" ")

    io.write('\n')

    if hora_tsumo.han == hora_ron.han == 0:
        io.write("和牌，但是无役")
        return

    if hora.pattern.menzen:
        # 保证排序的稳定性（单测需要）
        ordered_yaku = sorted(hora_ron.yaku | hora_tsumo.yaku, key=lambda y: (y.han, y), reverse=True)
    else:
        ordered_yaku = sorted(hora_ron.yaku | hora_tsumo.yaku, key=lambda y: (y.han - y.furo_loss, y), reverse=True)

    yakuman_tsumo = 0
    yakuman_ron = 0

    for yaku in ordered_yaku:
        allow_ron = yaku in hora_ron.yaku
        allow_tsumo = yaku in hora_tsumo.yaku

        io.write(yaku_mapping[yaku])
        io.write('  ')
        if yaku.is_yakuman:
            if yaku.han == 13:
                io.write("役满")
                if allow_ron:
                    yakuman_ron += 1
                if allow_tsumo:
                    yakuman_tsumo += 1
            else:
                io.write("两倍役满")
                if allow_ron:
                    yakuman_ron += 2
                if allow_tsumo:
                    yakuman_tsumo += 2
        else:
            if hora.pattern.menzen:
                io.write(str(yaku.han))
            else:
                io.write(str(yaku.han - yaku.furo_loss))
            io.write("番")

        if allow_ron and not allow_tsumo:
            io.write("  （荣和限定）")
        if not allow_ron and allow_tsumo:
            io.write("  （自摸限定）")

        io.write('\n')

    if yakuman_ron == 0 and hora.dora > 0:
        io.write("宝牌  ")
        io.write(str(hora.dora))
        io.write("番")

        if yakuman_tsumo != 0:
            # 自摸役满，荣和非役满的情况
            io.write("  （荣和限定）")

        io.write('\n')

    io.write('\n')

    if yakuman_ron == yakuman_tsumo:
        if yakuman_ron > 0:
            map_yakuman_text(io, yakuman_ron)
        else:
            if hora_ron.han == hora_tsumo.han and hora_ron.hu == hora_tsumo.hu:
                map_han_hu_text(io, hora.han, hora.hu)
            else:
                io.write("自摸：")
                map_han_hu_text(io, hora_tsumo.han, hora_tsumo.hu)
                io.write("\n荣和：")
                map_han_hu_text(io, hora_ron.han, hora_ron.hu)
    else:
        io.write("自摸：")
        if yakuman_tsumo > 0:
            map_yakuman_text(io, yakuman_tsumo)
        else:
            map_han_hu_text(io, hora_tsumo.han, hora_tsumo.hu)

        io.write("\n荣和：")
        if yakuman_ron > 0:
            map_yakuman_text(io, yakuman_ron)
        else:
            map_han_hu_text(io, hora_ron.han, hora_ron.hu)

    io.write("\n\n")

    if hora.self_wind == Wind.east or hora.self_wind is None:
        if hora_tsumo.parent_point == hora_ron.parent_point:
            parent_point = hora.parent_point
        else:
            parent_point = hora_ron.parent_point[0], hora_tsumo.parent_point[1]
    else:
        parent_point = None

    if hora.self_wind != Wind.east or hora.self_wind is None:
        if hora_tsumo.child_point == hora_ron.child_point:
            child_point = hora.child_point
        else:
            child_point = hora_ron.child_point[0], hora_tsumo.child_point[1], hora_tsumo.child_point[2]
    else:
        child_point = None

    map_han_hu(io, parent_point, child_point)
