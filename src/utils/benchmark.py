def bm_run_time(func):
    '''
    Calculate the runtime between two time points.
    '''
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
    async def warp():
        start_time = time.perf_counter()
        await func()
        end_time = time.perf_counter()
        print(f"Async Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
    return warp