from pathlib import Path
from typing import Optional

from mahjong_utils.bridge.webapi_jar.path import set_mahjongutils_webapi_jar_path
from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    mahjong_utils_send_image: bool = True
    mahjong_utils_webapi_jar: Optional[str]

    mahjong_utils_test: bool = False

    class Config:
        extra = "ignore"


conf = Config(**get_driver().config.dict())
if conf.mahjong_utils_webapi_jar:
    set_mahjongutils_webapi_jar_path(Path(conf.mahjong_utils_webapi_jar))
