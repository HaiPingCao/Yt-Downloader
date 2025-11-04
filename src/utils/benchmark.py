def bm_run_time(func):
    '''
    Calculate the runtime between two time points.
    '''
    # elapsed_time = end_time - start_time
    # hours, rem = divmod(elapsed_time, 3600)
    # minutes, seconds = divmod(rem, 60)
    # return f"{int(hours):02}:{int(minutes):02}:{seconds:05.2f}"
    def warp():
        import time
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
    return warp

def bm_async_run_time(func):
    '''
    Calculate the runtime between two time points for async functions.
    '''
    import time
    import asyncio
    async def warp():
        start_time = time.perf_counter()
        await func()
        end_time = time.perf_counter()
        print(f"Async Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
    return warp