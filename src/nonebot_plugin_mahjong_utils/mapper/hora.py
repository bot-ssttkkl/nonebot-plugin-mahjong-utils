from typing import TextIO, Optional, Tuple, Set

from mahjong_utils.hora import Hora
from mahjong_utils.models.tile import Tile
from mahjong_utils.models.wind import Wind
from mahjong_utils.point_by_han_hu import ParentPoint, ChildPoint
from mahjong_utils.yaku import Yaku

from nonebot_plugin_mahjong_utils.mapper.general import num_mapping, wind_mapping, yaku_mapping
from nonebot_plugin_mahjong_utils.mapper.hand import map_hand
from nonebot_plugin_mahjong_utils.mapper.point_by_han_hu import map_point_by_han_hu


def map_han_hu(io: TextIO, han: int, hu: int):
    io.write(f"{han}番{hu}符")


def map_yakuman_text(io: TextIO, yakuman: int):
    io.write(f"{num_mapping[yakuman]}倍役满")


def map_hora_basic_info(io: TextIO, hora: Hora, *, got: Optional[Tile] = None):
    map_hand(io, hora.pattern, got=got)

    if hora.dora > 0:
        io.write(f"dora{hora.dora} ")

    if hora.self_wind is not None:
        io.write(f"自风{wind_mapping[hora.self_wind]} ")

    if hora.round_wind is not None:
        io.write(f"场风{wind_mapping[hora.round_wind]} ")


def map_hora_yaku(
        io: TextIO, yaku_ron: Set[Yaku], yaku_tsumo: Set[Yaku],
        *, menzen: bool, dora: int
) -> Tuple[int, int]:
    merged_yaku = yaku_ron | yaku_tsumo

    if menzen:
        # 保证排序的稳定性（单测需要）
        ordered_yaku = sorted(merged_yaku, key=lambda y: (y.han, y), reverse=True)
    else:
        ordered_yaku = sorted(merged_yaku, key=lambda y: (y.han - y.furo_loss, y), reverse=True)

    yakuman_tsumo = 0
    yakuman_ron = 0

    for yaku in ordered_yaku:
        allow_ron = yaku in yaku_ron
        allow_tsumo = yaku in yaku_tsumo

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
            if menzen:
                io.write(str(yaku.han))
            else:
                io.write(str(yaku.han - yaku.furo_loss))
            io.write("番")

        if allow_ron and not allow_tsumo:
            io.write("  （荣和限定）")
        if not allow_ron and allow_tsumo:
            io.write("  （自摸限定）")

        io.write('\n')

    if yakuman_ron == 0 and dora > 0:
        io.write(f"宝牌  {dora}番")

        if yakuman_tsumo != 0:
            # 自摸役满，荣和非役满的情况
            io.write("  （荣和限定）")

        io.write('\n')

    return yakuman_ron, yakuman_tsumo


def map_hora(io: TextIO, hora_ron: Hora, hora_tsumo: Hora, *, got: Optional[Tile] = None):
    hora = hora_ron

    map_hora_basic_info(io, hora, got=got)
    io.write('\n')

    if hora.han == 0:
        io.write("和牌，但是无役")
        return

    yakuman_ron, yakuman_tsumo = map_hora_yaku(
        io,
        hora_ron.yaku,
        hora_tsumo.yaku,
        menzen=hora.pattern.menzen,
        dora=hora.dora
    )
    io.write('\n')

    if yakuman_ron == yakuman_tsumo:
        if yakuman_ron:
            map_yakuman_text(io, yakuman_ron)
        elif hora_ron.han == hora_tsumo.han and hora_ron.hu == hora_tsumo.hu:
            map_han_hu(io, hora_ron.han, hora_ron.hu)
        else:
            io.write("自摸：")
            map_han_hu(io, hora_tsumo.han, hora_tsumo.hu)
            io.write("\n荣和：")
            map_han_hu(io, hora_ron.han, hora_ron.hu)
    else:
        io.write("自摸：")
        if yakuman_tsumo:
            map_yakuman_text(io, yakuman_tsumo)
        else:
            map_han_hu(io, hora_tsumo.han, hora_tsumo.hu)

        io.write("\n荣和：")
        if yakuman_ron > 0:
            map_yakuman_text(io, yakuman_ron)
        else:
            map_han_hu(io, hora_ron.han, hora_ron.hu)

    io.write("\n\n")

    if hora_ron.self_wind == Wind.east or hora_ron.self_wind is None:
        parent_point = ParentPoint(hora_ron.parent_point.ron, hora_tsumo.parent_point.tsumo)
    else:
        parent_point = None

    if hora_ron.self_wind != Wind.east or hora_ron.self_wind is None:
        child_point = ChildPoint(hora_ron.child_point.ron, hora_tsumo.child_point.tsumo_parent,
                                 hora_tsumo.child_point.tsumo_child)
    else:
        child_point = None

    map_point_by_han_hu(io, parent_point, child_point)
