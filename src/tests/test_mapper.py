from io import StringIO
from typing import List, Mapping, Any, Optional

from mahjong_utils.hora import build_hora_from_shanten_result
from mahjong_utils.models.furo import Furo
from mahjong_utils.models.tile import parse_tiles, Tile
from mahjong_utils.shanten import shanten

from tests import MyTest


class BaseTestMapper(MyTest):
    tiles: List[Tile]
    furo: Optional[List[Furo]] = None
    kwargs: Mapping[str, Any] = {}
    excepted: str

    def test_map_hora(self):
        from nonebot_plugin_mahjong_utils.mapper.hora import map_hora

        tiles = self.tiles
        shanten_result = shanten(tiles, self.furo)
        hora_ron = build_hora_from_shanten_result(shanten_result, tiles[-1], False, **self.kwargs)
        hora_tsumo = build_hora_from_shanten_result(shanten_result, tiles[-1], True, **self.kwargs)

        with StringIO() as sio:
            map_hora(sio, hora_ron, hora_tsumo, got=tiles[-1])

            excepted = self.excepted
            assert sio.getvalue() == excepted


class TestMapper1(BaseTestMapper):
    tiles = parse_tiles("111s456p777z11222p")
    excepted = """1122456p111s777z2p 
三暗刻  2番  （自摸限定）
门清自摸  1番  （自摸限定）
中  1番

自摸：4番50符
荣和：1番50符

亲家和牌时：
荣和：2400点
自摸：子家4000点（满贯，共12000点）

子家和牌时：
荣和：1600点
自摸：子家2000点，亲家4000点（满贯，共8000点）"""


class TestMapper2(BaseTestMapper):
    tiles = parse_tiles("111s444p777z11222p")
    excepted = """1122444p111s777z2p 
四暗刻  役满  （自摸限定）
对对和  2番  （荣和限定）
三暗刻  2番  （荣和限定）
中  1番  （荣和限定）

自摸：一倍役满
荣和：5番60符

亲家和牌时：
荣和：12000点（满贯）
自摸：子家16000点（役满，共48000点）

子家和牌时：
荣和：8000点（满贯）
自摸：子家8000点，亲家16000点（役满，共32000点）"""


class TestMapper3(BaseTestMapper):
    tiles = parse_tiles("111s444p777z11222p")
    kwargs = {"dora": 8}
    excepted = """1122444p111s777z2p dora8 
四暗刻  役满  （自摸限定）
对对和  2番  （荣和限定）
三暗刻  2番  （荣和限定）
中  1番  （荣和限定）
宝牌  8番  （荣和限定）

自摸：一倍役满
荣和：13番60符

亲家和牌时：
荣和：48000点（役满）
自摸：子家16000点（役满，共48000点）

子家和牌时：
荣和：32000点（役满）
自摸：子家8000点，亲家16000点（役满，共32000点）"""


class TestMapper4(BaseTestMapper):
    tiles = parse_tiles("444p567s22333p")
    furo = [Furo.parse("234s")]
    excepted = """2233444p567s3p 234s 
断幺  1番

1番30符

亲家和牌时：
荣和：1500点
自摸：子家500点（共1500点）

子家和牌时：
荣和：1000点
自摸：子家300点，亲家500点（共1100点）"""


class TestMapper5(BaseTestMapper):
    tiles = parse_tiles("567s22333m")
    furo = [Furo.parse("0220s"), Furo.parse("234p")]
    excepted = """2233m567s3m 0220s 234p 
断幺  1番

自摸：1番50符
荣和：1番40符

亲家和牌时：
荣和：2000点
自摸：子家800点（共2400点）

子家和牌时：
荣和：1300点
自摸：子家400点，亲家800点（共1600点）"""
