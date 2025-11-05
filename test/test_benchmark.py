import sys
import asyncio
import time

# Ensure src is on sys.path so we can import utils
sys.path.append(r'd:\Dev\Python\python-youtube-downloader\src')

from utils.benchmark import bm_run_time, bm_async_run_time

@bm_async_run_time
async def foo(x):
    await asyncio.sleep(0.01)
    return x * 2

@bm_run_time
def bar(x):
    time.sleep(0.01)
    return x + 1

async def main():
    r1 = await foo(3)
    print("foo returned:", r1)
    r2 = bar(4)
    print("bar returned:", r2)

if __name__ == '__main__':
    asyncio.run(main())
