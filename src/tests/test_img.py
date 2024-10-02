from io import StringIO
from pathlib import Path

import pytest
from nonebot.adapters.onebot.v11 import Message
from nonebot.message import handle_event
from nonebug import App

from tests.utils import mock_obv11_message_event, create_obv11_bot


def strip_html(html: str) -> str:
    with StringIO() as sio:
        for line in html.split("\n"):
            sio.write(line.strip())
        return sio.getvalue()


async def do_test_img_result(app: App, message: str, expect_html_path: str):
    from nonebot_plugin_mahjong_utils.config import conf
    conf.mahjong_utils_send_image = True

    async with app.test_api() as ctx:
        from nonebot_plugin_mahjong_utils.mapper.sent_store import last_sent

        bot = create_obv11_bot(ctx)
        event = mock_obv11_message_event(Message(message))
        await handle_event(bot=bot, event=event)

    assert last_sent["html"] is not None
    # print(last_sent["html"])
    actual_html = strip_html(last_sent["html"])

    with open(expect_html_path, "r", encoding="utf-8") as f:
        expect_html = strip_html(f.read())
    assert actual_html == expect_html


@pytest.mark.asyncio
async def test_hora_img(app: App):
    await do_test_img_result(app, "11123456789999s",
                             str(Path(__file__).parent / "expect_html" / "hora_11123456789999s.html"))


@pytest.mark.asyncio
async def test_shanten_with_got_img(app: App):
    await do_test_img_result(app, "234567s12334p",
                             str(Path(__file__).parent / "expect_html" / "shanten_234567s12334p.html"))


@pytest.mark.asyncio
async def test_shanten_without_got_img(app: App):
    await do_test_img_result(app, "234567s1234p",
                             str(Path(__file__).parent / "expect_html" / "shanten_234567s1234p.html"))
