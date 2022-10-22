from functools import wraps
from typing import Type

from nonebot import logger
from nonebot.exception import MatcherException
from nonebot.internal.matcher import Matcher

from .errors import BadRequestError


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
            except Exception as e:
                logger.exception(e)
                await matcher.finish(f"内部错误：{type(e)}{str(e)}")

        return wrapped_func

    return decorator
