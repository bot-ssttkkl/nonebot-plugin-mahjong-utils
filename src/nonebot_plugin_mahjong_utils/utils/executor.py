import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from multiprocessing import cpu_count

my_executor = ThreadPoolExecutor(max_workers=cpu_count(), thread_name_prefix="nonebot-plugin-mahjong-utils")


async def run_in_my_executor(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    task = loop.run_in_executor(my_executor, partial(func, *args, **kwargs))
    return await task
