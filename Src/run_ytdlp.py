from core import yt, queue
from core.options import Options
import yt_dlp
# import re
# py -3 -m pip install -U --pre "yt-dlp[default]"

tempf_path: str = "\\Temp"
# yt_url: str = "https://www.youtube.com/watch?v=nl28drtdzpc" # input("Enter video URL: ")
yt_url: str = "https://www.youtube.com/playlist?list=PLKXe1HzhulvM7IuvwKMp_odaqg7VjFvJ5" # input("Enter video URL: ")

def fn1(link = yt_url):
    try:
        option = Options(mode=2, playlist=True, debug=False)
        info = yt.Info(url=link, option=option)
        _queue = queue.Queue()
        _queue.loop = 1
        
        # print(info)
        for inf in range(0, len(info)):
            # print(info[inf])
            _queue.add(info[inf])
            inf +=1

        print(_queue)
        print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        _queue.shuffle()
        print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(_queue)
        
        
        print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(_queue.nowplaying())
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        _queue.next()
        print(_queue.nowplaying())
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        _queue.next()
        print(_queue.nowplaying())
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        _queue.next()
        print(_queue.nowplaying())
        
        
    except Exception as e:
        print(f"Error: {e}")

    


def main(link = yt_url):
    fn1(link)

if __name__ == '__main__':
    main(link=yt_url)
