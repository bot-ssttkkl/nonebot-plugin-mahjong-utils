import time
import asyncio
from functools import partial
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor

from nonebot import logger

my_executor = ThreadPoolExecutor(
    max_workers=cpu_count(), thread_name_prefix="nonebot-plugin-mahjong-utils"
)


async def run_in_my_executor(func, *args, **kwargs):
    t = time.time()
    loop = asyncio.get_running_loop()
    task = loop.run_in_executor(my_executor, partial(func, *args, **kwargs))
    result = await task
    logger.opt(colors=True).debug(
        f"<y>{func.__name__}</y> cost {round(time.time() - t, 2)}s"
    )
    return result
