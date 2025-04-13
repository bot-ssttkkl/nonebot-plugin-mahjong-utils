import pytest
from nonebug import App
from nonebot.message import handle_event
from nonebot.adapters.onebot.v11 import Message

from tests.utils import create_obv11_bot, mock_obv11_message_event


async def do_test_text_result(app: App, message: str, expect: str):
    from nonebot_plugin_mahjong_utils.config import conf

    conf.mahjong_utils_send_image = False

    async with app.test_api() as ctx:
        from nonebot_plugin_mahjong_utils.mapper import last_sent

        bot = create_obv11_bot(ctx)
        event = mock_obv11_message_event(Message(message))
        await handle_event(bot=bot, event=event)
    assert last_sent["text"] == expect


@pytest.mark.asyncio
async def test_hora_text(app: App):
    await do_test_text_result(
        app,
        "11123456789999s 天和 自风东 场风东 dora1234",
        "11123456789999s dora1234 自风东 场风东 \n手牌拆解：\n  雀头：1s1s\n  面子：123s 456s 789s 999s\n\n自摸时：\n  役种：天和 纯正九莲宝灯\n  番数：3倍役满\n  符数：30\n  亲家和牌：子家48000点（3倍役满，共144000点）\n  子家和牌：子家24000点，亲家48000点（3倍役满，共96000点）\n\n荣和时：\n  役种：天和 纯正九莲宝灯\n  番数：3倍役满\n  符数：40\n  亲家和牌：144000点（3倍役满）\n  子家和牌：96000点（3倍役满）\n",
    )


@pytest.mark.asyncio
async def test_shanten_with_got_text(app: App):
    await do_test_text_result(
        app,
        "234567s12334p",
        "1233p234567s4p \n\n听牌：\n[打3p]  进张：14p (6张)\n好型改良：1s（打1p/4p，听9张）\n2s（打1p/4p，听9张）\n4s（打1p/4p，听9张）\n5s（打1p/4p，听9张）\n7s（打1p/4p，听9张）\n8s（打1p/4p，听9张）\n[打4p]  进张：3p (2张)\n好型改良：1p（打3p，听5张）\n4p（打3p，听5张）\n1s（打3p，听9张）\n2s（打3p，听9张）\n4s（打3p，听9张）\n5s（打3p，听9张）\n7s（打3p，听9张）\n8s（打3p，听9张）\n[打1p]  进张：3p (2张)\n好型改良：1p（打3p，听5张）\n2p（打3p，听6张）\n4p（打3p，听5张）\n5p（打2p/3p，听6张）\n1s（打3p，听9张）\n2s（打3p，听9张）\n4s（打3p，听9张）\n5s（打3p，听9张）\n7s（打3p，听9张）\n8s（打3p，听9张）\n\n1向听（退向）：\n[打2s]  进张：12345p2345678s (37张，好型37张)\n[打7s]  进张：12345p1234567s (37张，好型37张)\n[打4s]  进张：12345p1234s (28张，好型21张)\n[打5s]  进张：12345p5678s (28张，好型21张)\n[打3s]  进张：12345p2347s (27张，好型19张)\n[打6s]  进张：12345p2567s (27张，好型19张)\n[打2p]  进张：123456p (19张，好型12张)\n\n",
    )


@pytest.mark.asyncio
async def test_shanten_without_got_text(app: App):
    await do_test_text_result(
        app,
        "234567s1234p",
        "1234p234567s \n\n听牌：\n进张：14p (6张)\n好型改良：1s（打1p/4p，听9张）\n2s（打1p/4p，听9张）\n4s（打1p/4p，听9张）\n5s（打1p/4p，听9张）\n7s（打1p/4p，听9张）\n8s（打1p/4p，听9张）",
    )


@pytest.mark.asyncio
async def test_han_hu_text(app: App):
    await do_test_text_result(
        app,
        "3番40符",
        "3番40符\n亲家和牌时：\n荣和：7700点\n自摸：子家2600点（共7800点）\n\n子家和牌时：\n荣和：5200点\n自摸：子家1300点，亲家2600点（共5200点）",
    )
