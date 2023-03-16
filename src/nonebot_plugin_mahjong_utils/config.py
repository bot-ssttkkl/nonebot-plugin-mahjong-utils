from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    mahjong_utils_send_image: bool = False

    class Config:
        extra = "ignore"


conf = Config(**get_driver().config.dict())
