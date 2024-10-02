from pathlib import Path
from uuid import uuid4

import cv2
import pytest
from nonebot.adapters.onebot.v11 import Message
from nonebot.message import handle_event

from nonebug import App
from skimage.metrics import structural_similarity

from tests.utils import mock_obv11_message_event, create_obv11_bot


def compare_image(actual_img, expect_img):
    height, width = expect_img.shape[:2]
    actual_img = cv2.resize(actual_img, (width, height))

    # Convert images to grayscale
    actual_img_gray = cv2.cvtColor(actual_img, cv2.COLOR_BGR2GRAY)
    expect_img_gray = cv2.cvtColor(expect_img, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(actual_img_gray, expect_img_gray, full=True)
    return score


async def do_test_img_result(app: App, message: str, expect_path: str):
    from nonebot_plugin_mahjong_utils.config import conf
    conf.mahjong_utils_send_image = True

    async with app.test_api() as ctx:
        from nonebot_plugin_mahjong_utils.mapper import last_sent

        bot = create_obv11_bot(ctx)
        event = mock_obv11_message_event(Message(message))
        await handle_event(bot=bot, event=event)

    assert last_sent["img"] is not None

    actual_path = f"tmp/{uuid4()}.png"
    Path(actual_path).parent.mkdir(parents=True, exist_ok=True)
    with open(actual_path, "wb+") as f:
        f.write(last_sent["img"])

    try:
        actual_img = cv2.imread(actual_path)
        expect_img = cv2.imread(expect_path)

        ssim = compare_image(actual_img, expect_img)
        print(f"SSIM: {ssim}")
        assert ssim > 0.98
    finally:
        Path(actual_path).unlink(missing_ok=True)


@pytest.mark.asyncio
async def test_hora_img(app: App):
    await do_test_img_result(app, "11123456789999s",
                             str(Path(__file__).parent / "img" / "hora_11123456789999s.jpeg"))

#
# @pytest.mark.asyncio
# async def test_shanten_with_got_img(app: App):
#     await do_test_img_result(app, "234567s12334p",
#                              "1233p234567s4p \n\n听牌：\n[打3p]  进张：14p (6张)\n好型改良：1s（打1p/4p，听9张）\n2s（打1p/4p，听9张）\n4s（打1p/4p，听9张）\n5s（打1p/4p，听9张）\n7s（打1p/4p，听9张）\n8s（打1p/4p，听9张）\n[打4p]  进张：3p (2张)\n好型改良：1p（打3p，听5张）\n4p（打3p，听5张）\n1s（打3p，听9张）\n2s（打3p，听9张）\n4s（打3p，听9张）\n5s（打3p，听9张）\n7s（打3p，听9张）\n8s（打3p，听9张）\n[打1p]  进张：3p (2张)\n好型改良：1p（打3p，听5张）\n2p（打3p，听6张）\n4p（打3p，听5张）\n5p（打2p/3p，听6张）\n1s（打3p，听9张）\n2s（打3p，听9张）\n4s（打3p，听9张）\n5s（打3p，听9张）\n7s（打3p，听9张）\n8s（打3p，听9张）\n\n1向听（退向）：\n[打2s]  进张：12345p2345678s (37张，好型37张)\n[打7s]  进张：12345p1234567s (37张，好型37张)\n[打4s]  进张：12345p1234s (28张，好型21张)\n[打5s]  进张：12345p5678s (28张，好型21张)\n[打3s]  进张：12345p2347s (27张，好型19张)\n[打6s]  进张：12345p2567s (27张，好型19张)\n[打2p]  进张：123456p (19张，好型12张)\n\n")
#
#
# @pytest.mark.asyncio
# async def test_shanten_without_got_img(app: App):
#     await do_test_img_result(app, "234567s1234p",
#                              "1234p234567s \n\n听牌：\n进张：14p (6张)\n好型改良：1s（打1p/4p，听9张）\n2s（打1p/4p，听9张）\n4s（打1p/4p，听9张）\n5s（打1p/4p，听9张）\n7s（打1p/4p，听9张）\n8s（打1p/4p，听9张）")
#
#
# @pytest.mark.asyncio
# async def test_han_hu_img(app: App):
#     await do_test_img_result(app, "3番40符",
#                              "3番40符\n亲家和牌时：\n荣和：7700点\n自摸：子家2600点（共7800点）\n\n子家和牌时：\n荣和：5200点\n自摸：子家1300点，亲家2600点（共5200点）")
