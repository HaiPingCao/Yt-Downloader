from core.yt import Info
from core.yt_options import Options
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio


app = FastAPI()

# Turn off CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_info(url:str, start_index:int=0, end_index:int=0):
    info_out = []
    for i in range(start_index, end_index):
        i += 1
        options = Options(mode=2, playlist=True, debug=False, playlist_items_index=f"{i}-{i}")
        info = await Info(url, options, write_json=False)
        info_out.append(info)
    return info_out


@app.websocket("/ws/music_info")
async def ws_music_info(ws: WebSocket):
    await ws.accept()
    
    try:
        params = await ws.receive_json()
        url = params["url"]
        start = params.get("v_start")
        end = params.get("v_end")

        info_list = []
        
        for i in range(start, end + 1):
            info = await get_info(url, i, i + 1)
            info_list.append(info[0])
            
            # Use len(info_list) - 1 as index, not i
            idx = len(info_list) - 1
            ws_info = {
                "index": i,
                "duration": str(info_list[idx][0][2]),
                "title": str(info_list[idx][0][0]),
                "audio_url": str(info_list[idx][0][3])
            }
            
            await ws.send_json(ws_info)
        
        # Send completion signal
        await ws.send_json({"status": "complete"})
        
        # Small delay before closing
        await asyncio.sleep(0.1)
        
    except Exception as e:
        await ws.send_json({"error": str(e)})
    finally:
        await ws.close()


