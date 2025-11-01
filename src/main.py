from core.yt import Info
from core.yt_options import Options
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware


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
     # Chấp nhận kết nối WebSocket từ client
     await ws.accept()

     # Nhận dữ liệu JSON ban đầu từ client (gồm url, v_start, v_end)
     params = await ws.receive_json()

     info_list = []  # Danh sách để lưu kết quả từng video

     # Lấy các tham số từ client gửi lên
     url = params["url"]
     start = params.get("v_start")
     end = params.get("v_end")

     # Lặp qua từng video trong khoảng [start, end]
     for i in range(start, end + 1):
          info = await get_info(url, i, i + 1)
          info_list.append(info[0])

          # Tạo dữ liệu giả để gửi dần về client qua WebSocket
          ws_info = {
               "index": i,
               "duration": f"{info_list[i][0][2]}",
               "title": f"{info_list[i][0][0]}",
               "audio_url": f"{info_list[i][0][3]}"
          }

          # Gửi JSON từng bài nhạc về client (frontend sẽ hiển thị dần)
          await ws.send_json(ws_info)

     # Sau khi gửi hết dữ liệu thì đóng kết nối WebSocket
     await ws.close()


