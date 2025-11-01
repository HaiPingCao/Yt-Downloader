from core.yt import Info
from core.yt_options import Options
import asyncio


async def get_info(url:str, start_index:int=0, end_index:int=0):
    info_out = []
    for i in range(start_index, end_index):
        i += 1
        options = Options(mode=2, playlist=True, debug=False, playlist_items_index=f"{i}-{i}")
        info = await Info(url, options, write_json=False)
        info_out.append(info)
    return info_out


def main():
    url = "http://youtube.com/playlist?list=PLKXe1HzhulvM7IuvwKMp_odaqg7VjFvJ5"
    outp = []
    pl_cap = 3
    
    for i in range(0, pl_cap):
        info = asyncio.run(get_info(url, i, i+1))
        outp.append(info[0])
        print("\n-----------------------\n")
        print(info[0])
    
if __name__ == "__main__":
    main()