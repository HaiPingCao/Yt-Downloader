import time
import asyncio
import functools


def bm_run_time(func):
    '''
    Calculate the runtime between two time points for synchronous functions.
    The wrapper accepts any positional and keyword arguments and returns the
    wrapped function's result.
    '''
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
        return result

    return wrap


def bm_async_run_time(func):
    '''
    Calculate the runtime between two time points for async functions.
    The async wrapper accepts any positional and keyword arguments and returns
    the wrapped coroutine's result.
    '''
    @functools.wraps(func)
    async def wrap(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Async Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
        return result

    return wrap