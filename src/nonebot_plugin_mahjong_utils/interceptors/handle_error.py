from functools import wraps
from typing import Type

from nonebot import logger
from nonebot.exception import MatcherException, ActionFailed
from nonebot.internal.matcher import Matcher

from nonebot_plugin_mahjong_utils.errors import BadRequestError


def handle_error(matcher: Type[Matcher]):
    def decorator(func):
        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except MatcherException as e:
                raise e
            except BadRequestError as e:
                await matcher.finish(e.message)
            except ActionFailed as e:
                # 避免当发送消息错误时再尝试发送
                logger.exception(e)
            except Exception as e:
                logger.exception(e)
                await matcher.finish(f"内部错误：{type(e)}{str(e)}")

        return wrapped_func

    return decorator
