"""
nonebot-plugin-mahjong-utils

@Author         : ssttkkl
@License        : MIT
@GitHub         : https://github.com/ssttkkl/nonebot-plugin-mahjong-utils
"""

help_text = """
手牌分析：
- 输入手牌代码，输出向听数（未摸牌状态）、牌理（已摸牌、未和牌状态）或和牌分析（已摸牌、已和牌状态）。
- 手牌代码的最后一张牌作为所和的牌，手牌代码后可通过空格分割输入副露、自风、场风、dora、额外役。暗杠通过0990m的格式输入。
- 例：23445633p777s 0990m 立直 一发 dora3

番符点数查询：
- 输入x番y符，输出亲家/子家的自摸/荣和得点
""".strip()

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name='麻将小工具',
    description='手牌分析、番符点数查询、……',
    usage=help_text,
    extra={'version': '0.1.5'}
)

from . import matchers
