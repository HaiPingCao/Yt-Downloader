from core.yt import Info
from core.options import Options


def run_yt():    
     url = "https://www.youtube.com/watch?v=Lotg1En0EFU&list=RDLotg1En0EFU&start_radio=1"

     # options = Options(mode=2, playlist=True, debug=True, playlist_items_index="1-5")
     # info = Info(url, options, write_json=True)

     
     for i in range(1,5):
          options = Options(mode=2, playlist=True, debug=False, playlist_items_index=f"{i}-{i}")
          info = Info(url, options)
          print(info)

if __name__ == '__main__':
     run_yt()