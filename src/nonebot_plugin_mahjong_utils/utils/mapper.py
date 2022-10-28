from collections import defaultdict
from typing import TextIO, Optional, Tuple

from mahjong_utils.hora import Hora
from mahjong_utils.models.hand import Hand, RegularHand
from mahjong_utils.models.tile import tiles_text, Tile
from mahjong_utils.models.wind import Wind
from mahjong_utils.shanten import ShantenResult
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
    haitei: "海底捞月",
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
    churen9: "纯正九莲宝灯",
    suanko_tanki: "四暗刻单骑",
    kokushi13: "国士无双十三面"
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


def map_hand(io: TextIO, hand: Hand, *, got: Optional[Tile] = None):
    tiles = sorted(hand.tiles)

    if isinstance(hand, RegularHand):
        for fr in hand.furo:
            for t in fr.tiles:
                tiles.remove(t)

    if got is not None:
        tiles.remove(got)
        tiles.append(got)

    io.write(tiles_text(tiles))
    io.write(' ')

    if isinstance(hand, RegularHand):
        for fr in hand.furo:
            io.write(str(fr))
            io.write(' ')


def map_shanten_result(io: TextIO, result: ShantenResult, *, got: Optional[Tile] = None):
    map_hand(io, result.hands[0], got=got)
    io.write('\n')

    if result.shanten == 0:
        io.write("听牌")
    else:
        io.write("向听数：")
        io.write(str(result.shanten))
    io.write("\n")

    remaining = defaultdict(lambda: 4)
    for t in result.hands[0].tiles:
        remaining[t] -= 1

    if result.advance is not None:
        advance_count = 0
        for t in result.advance:
            advance_count += remaining[t]

        io.write("进张：")
        io.write(tiles_text(sorted(result.advance)))
        io.write(" (")
        io.write(str(advance_count))
        io.write("张)\n")
    else:
        ordered = []
        for discard, advance in result.discard_to_advance.items():
            advance_count = 0
            for t in advance:
                advance_count += remaining[t]
            ordered.append((discard, advance, advance_count))

        ordered.sort(key=lambda x: x[2], reverse=True)

        for discard, advance, advance_count in ordered:
            io.write("打")
            io.write(str(discard))
            io.write("\t")
            io.write("进张：")
            io.write(tiles_text(sorted(advance)))
            io.write(" (")
            io.write(str(advance_count))
            io.write("张)\n")


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
    map_hand(io, hora.hand, got=got)

    if hora.dora > 0:
        io.write("dora")
        io.write(str(hora.dora))
        io.write(" ")

    if hora.hand.self_wind is not None:
        io.write(wind_mapping[hora.hand.self_wind])
        io.write("家 ")

    if hora.hand.round_wind is not None:
        io.write("场风")
        io.write(wind_mapping[hora.hand.round_wind])
        io.write(" ")

    io.write('\n')

    if hora_tsumo.han == hora_ron.han == 0:
        io.write("和牌，但是无役")
        return

    if hora.hand.menzen:
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
            if hora.hand.menzen:
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
            if hora_ron.han == hora_tsumo.han and hora_ron.hand.hu == hora_tsumo.hand.hu:
                map_han_hu_text(io, hora.han, hora.hand.hu)
            else:
                io.write("自摸：")
                map_han_hu_text(io, hora_tsumo.han, hora_tsumo.hand.hu)
                io.write("\n荣和：")
                map_han_hu_text(io, hora_ron.han, hora_ron.hand.hu)
    else:
        io.write("自摸：")
        if yakuman_tsumo > 0:
            map_yakuman_text(io, yakuman_tsumo)
        else:
            map_han_hu_text(io, hora_tsumo.han, hora_tsumo.hand.hu)

        io.write("\n荣和：")
        if yakuman_ron > 0:
            map_yakuman_text(io, yakuman_ron)
        else:
            map_han_hu_text(io, hora_ron.han, hora_ron.hand.hu)

    io.write("\n\n")

    if hora.hand.self_wind == Wind.east or hora.hand.self_wind is None:
        if hora_tsumo.parent_point == hora_ron.parent_point:
            parent_point = hora.parent_point
        else:
            parent_point = hora_ron.parent_point[0], hora_tsumo.parent_point[1]
    else:
        parent_point = None

    if hora.hand.self_wind != Wind.east or hora.hand.self_wind is None:
        if hora_tsumo.child_point == hora_ron.child_point:
            child_point = hora.child_point
        else:
            child_point = hora_ron.child_point[0], hora_tsumo.child_point[1], hora_tsumo.child_point[2]
    else:
        child_point = None

    map_han_hu(io, parent_point, child_point)
