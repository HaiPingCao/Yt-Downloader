import asyncio
from asyncio import TaskGroup
import math

from core.yt import *
from core.yt_options import Options
from utils.link import *
from utils.benchmark import *


def get_info(url:str, v_start:int=1, v_end:int=2):    
    options = Options(mode=2, playlist=True, debug=False, playlist_items_index=f"{v_start}-{v_end}")
    info = extract_info(url, options)
    return info


@bm_async_run_time
async def process_info_v1(url:str, v_start:int=1, v_end:int=2):    
    info_out = []
    for i in range(v_start, v_end):
        # print(i)
        options = Options(mode=2, playlist=True, debug=False, playlist_items_index=f"{i}-{i}")
        try:
            info = await extract_info(url, options)
        except AttributeError as ex:
            print(f"Error extracting info for index {i}: {ex}")
            continue
        info_out.append(info)
    return info_out


@bm_async_run_time
async def process_info_v2(url, i_s, i_e):
    playlist_info = []
    
    # build indices list using i_s as 1-based start (default to 1 if i_s < 1)
    start_idx = i_s if isinstance(i_s, int) and i_s >= 1 else 1
    indices = list(range(start_idx, i_e + 1))

    i = 0
    try:
        while i < len(indices):
            # process a pair concurrently when possible
            if i + 1 < len(indices):
                idx1, idx2 = indices[i], indices[i + 1]
                t1 = asyncio.create_task(get_info(url, idx1, idx1))
                t2 = asyncio.create_task(get_info(url, idx2, idx2))
                res1, res2 = await asyncio.gather(t1, t2)
                playlist_info.extend([res1, res2])

            else:
                idx = indices[i]
                res = await get_info(url, idx, idx)
                playlist_info.append(res)
            i += 2
            return playlist_info
    except Exception as ex:
        print(f"Error processing info: {ex}")


# @bm_async_run_time
async def main():
    # url: str = "https://www.youtube.com/playlist?list=PLKXe1HzhulvPTufUVAapnT2k7KEFOLB1M"
    # url:str = "https://www.youtube.com/playlist?list=PLKXe1HzhulvOUsdLNo7sdhCFYam76rmrt"
    url:str = "https://www.youtube.com/watch?v=hCdBuTO1g1E&list=RDhCdBuTO1g1E&start_radio=1"
    

    _link_type = link_type(url)
    start = 0
    
    try:
        end = get_playlist_count(url)
    except ValueError as ex:
        end = 20
        print(f"Could not get playlist count: {ex}, defaulting to {end}")
        

    print(f"Link Type: {_link_type}, Total Items: {end}")
    print("Fetching info...\n")

    await process_info_v1(url, start, end)
    await process_info_v2(url, start, end)
    # print(Options(mode=2, playlist=False, debug=False, playlist_items_index=f"{start}-{end}"))


if __name__ == "__main__":
    asyncio.run(main())