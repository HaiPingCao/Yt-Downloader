import asyncio
from core.yt import *
from core.yt_options import Options
from utils.link import *
from utils.benchmark import *

async def get_info(url:str, v_start:int=1, v_end:int=2):    
    options = Options(mode=2, playlist=False, debug=False, playlist_items_index=f"{v_start}-{v_end}")
    info = extract_info(url, options)  # extract_info is synchronous, no await needed
    await asyncio.sleep(0)  # slight delay to avoid rate limiting
    return info

@bm_async_run_time
async def process_info_v1(url:str, v_start:int=1, v_end:int=2):    
    info_out = []
    for i in range(v_start, v_end):
        # print(i)
        options = Options(mode=2, playlist=True, debug=False, playlist_items_index=f"{i}-{i}")
        try:
            info = await get_info(url, i, i)  # Use async get_info instead of sync extract_info
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

    for i in range(0, len(indices), 4):
        # process a pair concurrently when possible
        if i + 1 < len(indices):
            idx1, idx2, idx3, idx4 = indices[i], indices[i + 1], indices[i + 2], indices[i + 3]
            print(f"{idx1},{idx2},{idx3},{idx4}")
            task1 = task2 = task3 = task4 = None  # Initialize task variables
            # create tasks for concurrent execution
            task1 = asyncio.create_task(get_info(url, idx1, idx1))
            task2 = asyncio.create_task(get_info(url, idx2, idx2))
            task3 = asyncio.create_task(get_info(url, idx3, idx3))
            task4 = asyncio.create_task(get_info(url, idx4, idx4))
            # await both tasks and handle exceptions
            try:
                result1, result2, result3, result4 = await asyncio.gather(task1, task2, task3, task4)
                playlist_info.extend([result1, result2, result3, result4])
                await asyncio.sleep(.1)  # slight delay to avoid rate limiting
            except AttributeError as ex:
                print(f"Error extracting info for indices {idx1},{idx2},{idx3},{idx4}: {ex}")
        else:
            idx = indices[i]
            try:
                res = await get_info(url, idx, idx)
            except AttributeError as ex:
                print(f"Error extracting info for index {idx}: {ex}")
                continue
            
            playlist_info.append(res)
    return playlist_info


@bm_async_run_time
async def process_info_v3(url, start_index, end_index):
    playlist_info = []
    # start_index phai >= 1
    # isintance(sthing, datatype) de kiem tra kieu du lieu
    start_idx = start_index if isinstance(start_index, int) and start_index >= 1 else 1
    # tao danh sach chi so tu start_index den end_index
    indices = list(range(start_idx, end_index + 1))
    # Chay vong lap qua danh sach chi so voi buoc nhay 4 (4 phan chay song song)
    for i in range(0, len(indices), 4):
        print(f"indices: {indices[i:i+4]}")
        # Create tasks for concurrent execution, handling remaining items < 4
        tasks = []
        for j in range(4):
            if i + j < len(indices):
                task = asyncio.create_task(get_info(url, indices[i + j], indices[i + j]))
                tasks.append(task)
        
        # Gather and await all tasks for this batch
        if tasks:
            results = await asyncio.gather(*tasks)
            playlist_info.extend(results)
            await asyncio.sleep(0)  # slight delay to avoid rate limiting
    return playlist_info

# @bm_async_run_time
async def main():
    # url: str = "https://www.youtube.com/playlist?list=PLKXe1HzhulvPTufUVAapnT2k7KEFOLB1M"
    url:str = "https://www.youtube.com/playlist?list=PLKXe1HzhulvOUsdLNo7sdhCFYam76rmrt"
    # url:str = "https://www.youtube.com/watch?v=Eug-A577g-U&list=PLKXe1HzhulvM7IuvwKMp_odaqg7VjFvJ5&pp=gAQB"

    _link_type = link_type(url)
    start = 0
    
    try:
        end = get_playlist_count(url)
    except ValueError as ex:
        end = 4
        print(f"Could not get playlist count: {ex}, defaulting to {end}")    

    print(f"Link Type: {_link_type}, Total Items: {end}")
    print("Fetching info...\n")

    # v1 = await process_info_v1(url, start, end)
    # v2 = await process_info_v2(url, start, end)
    v3 = await process_info_v3(url, start, end)
    with open("astest_output.json", "w", encoding="utf-8") as f:
        for item in v3:
            f.write(f"{item}\n")


if __name__ == "__main__":
    asyncio.run(main())