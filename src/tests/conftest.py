import pytest
import nonebot
from nonebot.adapters.onebot.v11 import Adapter


@pytest.fixture(scope="session", autouse=True)
def load_bot():
    # 加载适配器
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)

    # 加载插件
    plugins = nonebot.load_plugins("nonebot_plugin_mahjong_utils")

    from nonebot_plugin_mahjong_utils.config import conf
    conf.mahjong_utils_test = True

    return plugins
