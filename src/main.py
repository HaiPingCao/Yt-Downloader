import asyncio
import subprocess
from core.yt import Info
from core.yt_options import Options
from fastapi import FastAPI


app = FastAPI()


async def get_info(url:str, v_start:int=1, v_end:int=2):    
     info_out = []
     for i in range(v_start, v_end):
          options = Options(mode=2, playlist=True, debug=False, playlist_items_index=f"{i}-{i}")
          info = await Info(url, options, write_json=False)
          info_out.append(info)
     return info_out


@app.get("/music_info/")
async def get_video_info(url: str, v_start: int = 1, v_end: int = 5):
    info = await get_info(url, v_start, v_end)
    if info is None:
        return {"status": "Error: Could not fetch video info"}
    return info


if __name__ == '__main__':
     pass
# 