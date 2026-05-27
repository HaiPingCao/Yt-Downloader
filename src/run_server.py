from core.dispatcher import yt_dispatcher
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


@app.websocket("/ws/music")
async def ws_music_info(ws: WebSocket):
    await ws.accept()

    try:

        params = await ws.receive_json()
        url = params["url"]
        start_index = params.get("start_index") or None
        end_index = params.get("end_index") or None

        loop = asyncio.get_event_loop()

        def on_segment(segment):
            data = {
                "segment": f"{segment.start_index}-{segment.end_index}",
                "tracks": [track for track in segment.tracks],
                "success": segment.success,
                "error": segment.error,
            }
            # Ensure we schedule the coroutine on the main event loop from worker threads
            asyncio.run_coroutine_threadsafe(ws.send_json(data), loop)

        # Run the (potentially blocking) dispatcher in a background thread
        await asyncio.to_thread(
            yt_dispatcher,
            url=url,
            on_segment=on_segment,
            start_index=start_index,
            end_index=end_index,
        )

        # Send completion signal
        await ws.send_json({"status": "complete"})

        # Small delay before closing
        await asyncio.sleep(0.1)

    except Exception as e:
        await ws.send_json({"error": str(e)})
    finally:
        await ws.close()
