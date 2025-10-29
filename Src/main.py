from core.yt import Info
from core.options import Options
import json


def run_yt():    
     url = "https://www.youtube.com/watch?v=Lotg1En0EFU&list=RDLotg1En0EFU&start_radio=1"

     options = Options(mode=2, playlist=True, debug=True)
     info = Info(url, options)
     with open("buffer.json", "w") as f:
          json.dump(info, f, indent=4)

if __name__ == '__main__':
     run_yt()