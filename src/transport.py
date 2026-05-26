from core.dispatcher import *
from core.yt_dlp_options import build_options
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


async def get_info(url: str, start_index: int = 0, end_index: int = 0):
    info_out = []

    for i in range(start_index, end_index):
        i += 1
        options = build_options(
            mode="info", playlist=True, debug=False, playlist_items=f"{i}-{i}"
        )
        info = yt_dispatcher(url)
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

        # Limit concurrent fetches to avoid overwhelming the server
        semaphore = asyncio.Semaphore(3)

        async def fetch_and_send(index):
            async with semaphore:
                # Fetch video info
                info = await get_info(url, index, index + 1)

                # Prepare response
                ws_info = {
                    "index": index,
                    "duration": str(info[0][0][2]),
                    "title": str(info[0][0][0]),
                    "audio_url": str(info[0][0][3]),
                }

                # Send immediately
                await ws.send_json(ws_info)

                # Force flush to prevent buffering
                await asyncio.sleep(0)

        # Create all tasks at once
        tasks = [asyncio.create_task(fetch_and_send(i)) for i in range(start, end + 1)]

        # Wait for all to complete
        await asyncio.gather(*tasks)

        # Send completion signal
        await ws.send_json({"status": "complete"})

        # Small delay before closing
        await asyncio.sleep(0.1)

    except Exception as e:
        await ws.send_json({"error": str(e)})
    finally:
        await ws.close()
