from io import StringIO
from typing import List, Mapping, Any, Optional

from mahjong_utils.hora import build_hora_from_shanten_result
from mahjong_utils.models.furo import Furo, parse_furo
from mahjong_utils.models.tile import parse_tiles, Tile
from mahjong_utils.shanten import shanten

from tests import MyTest


class BaseTestMapper(MyTest):
    tiles: List[Tile]
    furo: Optional[List[Furo]] = None
    kwargs: Mapping[str, Any] = {}
    excepted: str

    def test_map_hora(self):
        from nonebot_plugin_mahjong_utils.utils.mapper import map_hora

        tiles = self.tiles
        shanten_result = shanten(tiles, self.furo)
        hora_ron = build_hora_from_shanten_result(shanten_result, tiles[-1], False, **self.kwargs)
        hora_tsumo = build_hora_from_shanten_result(shanten_result, tiles[-1], True, **self.kwargs)

        with StringIO() as sio:
            map_hora(sio, hora_ron, hora_tsumo, got=tiles[-1])

            excepted = self.excepted
            assert sio.getvalue() == excepted


class TestMapper1(BaseTestMapper):
    tiles = parse_tiles("111s456p777z1122p")
    excepted = """1122456p111s777z2p 
三暗刻  2番  （自摸限定）
门清自摸  1番  （自摸限定）
中  1番

自摸：4番50符  满贯
荣和：1番50符

亲家和牌时：自摸12000 (4000 ALL)，荣和2400
子家和牌时：自摸8000 (4000 2000)，荣和1600
"""


class TestMapper2(BaseTestMapper):
    tiles = parse_tiles("111s444p777z1122p")
    excepted = """1122444p111s777z2p 
四暗刻  役满  （自摸限定）
对对和  2番  （荣和限定）
三暗刻  2番  （荣和限定）
中  1番  （荣和限定）

自摸：一倍役满
荣和：5番60符  满贯

亲家和牌时：自摸48000 (16000 ALL)，荣和12000
子家和牌时：自摸32000 (16000 8000)，荣和8000
"""


class TestMapper3(BaseTestMapper):
    tiles = parse_tiles("111s444p777z1122p")
    kwargs = {"dora": 8}
    excepted = """1122444p111s777z2p dora8 
四暗刻  役满  （自摸限定）
对对和  2番  （荣和限定）
三暗刻  2番  （荣和限定）
中  1番  （荣和限定）
宝牌  8番  （荣和限定）

自摸：一倍役满
荣和：13番60符  累计役满

亲家和牌时：自摸48000 (16000 ALL)，荣和48000
子家和牌时：自摸32000 (16000 8000)，荣和32000
"""


class TestMapper4(BaseTestMapper):
    tiles = parse_tiles("444p567s22333p")
    furo = [parse_furo("234s")]
    excepted = """2233444p567s3p 234s 
断幺  1番

1番30符

亲家和牌时：自摸1500 (500 ALL)，荣和1500
子家和牌时：自摸1100 (500 300)，荣和1000
"""


class TestMapper5(BaseTestMapper):
    tiles = parse_tiles("567s22333m")
    furo = [parse_furo("0220s"), parse_furo("234p")]
    excepted = """2233m567s3m 0220s 234p 
断幺  1番

自摸：1番50符
荣和：1番40符

亲家和牌时：自摸2400 (800 ALL)，荣和2000
子家和牌时：自摸1600 (800 400)，荣和1300
"""
