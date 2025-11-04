import asyncio

from core.yt import *
from core.yt_options import Options
from utils.link import *
from utils.benchmark import *


async def get_info(url: str, start_index: int = 0, end_index: int = 0):
    async def fetch_single(index):
        options = Options(
            mode=2, 
            playlist=True, 
            debug=False, 
            playlist_items_index=f"{index}-{index}"
        )
        return await extract_info(url, options)
    
    # Create all tasks
    tasks = [fetch_single(i + 1) for i in range(start_index, end_index)]
    
    # Run all concurrently
    info_out = await asyncio.gather(*tasks)
    
    return info_out

@bm_async_run_time
async def main():
    url: str = "https://www.youtube.com/watch?v=oUHOyPvmLFU&list=RDoUHOyPvmLFU&start_radio=1"

    _link_type = link_type(url)
    start = 0
    
    try:
        end = get_playlist_count(url)
    except ValueError as ex:
        print(f"Could not get playlist count: {ex}, defaulting to 5")
        end = 5

    print(f"Link Type: {_link_type}, Total Items: {end}")
    print("Fetching info...\n")

    async def fetch_and_print(index):
        try:
            info = await get_info(url, index - 1, index)
            if info and len(info) > 0:
                title = info[0][0][0]
                duration = info[0][0][2]
                audio_url = info[0][0][3]
                print(f"{index}. {title} ({duration}s)")
            else:
                print(f"{index}. No info available")
        except Exception as e:
            print(f"{index}. Error: {e}")

    # Create all tasks
    tasks = [fetch_and_print(i + 1) for i in range(start, end)]
    
    # Run concurrently, print as each completes
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())