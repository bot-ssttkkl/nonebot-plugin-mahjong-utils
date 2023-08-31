#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.qqguild import Adapter as QQGuildAdapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(QQGuildAdapter)

nonebot.load_plugin("nonebot_plugin_mahjong_utils")

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run()
