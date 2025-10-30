from core.yt import Info
from core.yt_options import Options


def run_yt():    
     url = "https://music.youtube.com/watch?v=hE-XxWeYhPY&si=4tE2JPKgW90oRrpa"

     # options = Options(mode=2, playlist=True, debug=True, playlist_items_index="1-5")
     # info = Info(url, options, write_json=True)

     
     for i in range(1,2):
          options = Options(mode=2, playlist=True, debug=False, playlist_items_index=f"{i}-{i}")
          info = Info(url, options, write_json=True)
          print()
          print(info)

if __name__ == '__main__':
     run_yt()