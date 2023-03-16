from typing import TextIO, List

from mahjong_utils.hora import Hora, RegularHoraHandPattern
from mahjong_utils.models.furo import Furo
from mahjong_utils.models.tile import Tile

from nonebot_plugin_mahjong_utils.mapper.plaintext.general import num_mapping, wind_mapping, yaku_mapping
from nonebot_plugin_mahjong_utils.mapper.plaintext.hand import map_hand
from nonebot_plugin_mahjong_utils.mapper.plaintext.point_by_han_hu import get_tsumo_text, get_ron_text


def map_yakuman_text(io: TextIO, yakuman: int):
    io.write(f"{num_mapping[yakuman]}倍役满")


def map_hora_basic_info(io: TextIO, hora: Hora, tiles: List[Tile], furo: List[Furo]):
    map_hand(io, tiles, furo)

    if hora.dora > 0:
        io.write(f"dora{hora.dora} ")

    if hora.self_wind is not None:
        io.write(f"自风{wind_mapping[hora.self_wind]} ")

    if hora.round_wind is not None:
        io.write(f"场风{wind_mapping[hora.round_wind]} ")

    io.write('\n')


def map_regular_hora_hand_pattern(io: TextIO, pattern: RegularHoraHandPattern):
    io.write("手牌拆解：\n")
    io.write(f"  雀头：{pattern.jyantou}{pattern.jyantou}\n")
    if pattern.menzen_mentsu:
        io.write(f"  面子：{' '.join(map(lambda x: str(x), pattern.menzen_mentsu))}\n")
    if pattern.furo:
        io.write(f"  副露：{' '.join(map(lambda x: str(x), pattern.furo))}\n")


def map_han_hu(io: TextIO, hora: Hora):
    if hora.has_yakuman:
        io.write(f"  番数：{sum(map(lambda x: x.han, hora.yaku)) // 13}倍役满\n")
    else:
        io.write(f"  番数：{hora.han}番\n")
    io.write(f"  符数：{hora.hu}\n")


def map_hora(io: TextIO, hora_ron: Hora, hora_tsumo: Hora, tiles: List[Tile], furo: List[Furo]):
    hora = hora_ron

    map_hora_basic_info(io, hora, tiles, furo)
    if isinstance(hora.pattern, RegularHoraHandPattern):
        map_regular_hora_hand_pattern(io, hora.pattern)
    io.write('\n')

    io.write('自摸时：\n')
    if hora_tsumo == 0:
        io.write("  和牌，但是无役\n")
    else:
        io.write(f"  役种：{' '.join(map(lambda x: yaku_mapping[x], hora_tsumo.yaku))}\n")
        map_han_hu(io, hora_tsumo)
        io.write(f"  亲家和牌：{get_tsumo_text(0, hora_tsumo.parent_point.tsumo, True)}\n")
        io.write(
            f"  子家和牌：{get_tsumo_text(hora_tsumo.child_point.tsumo_parent, hora_tsumo.child_point.tsumo_child, False)}\n")

    io.write('\n')

    io.write('荣和时：\n')
    if hora_ron == 0:
        io.write("  和牌，但是无役\n")
    else:
        io.write(f"  役种：{' '.join(map(lambda x: yaku_mapping[x], hora_ron.yaku))}\n")
        map_han_hu(io, hora_ron)
        io.write(f"  亲家和牌：{get_ron_text(hora_ron.parent_point.ron, True)}\n")
        io.write(f"  子家和牌：{get_ron_text(hora_ron.child_point.ron, False)}\n")
