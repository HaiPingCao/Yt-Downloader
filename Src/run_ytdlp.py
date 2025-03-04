from core import yt_utils, link_utils
from core.options import Options
import yt_dlp
# import re
# py -3 -m pip install -U --pre "yt-dlp[default]"

tempf_path: str = "\\Temp"
yt_url: str = "https://www.youtube.com/watch?v=nl28drtdzpc" # input("Enter video URL: ")
# yt_url: str = "https://www.youtube.com/playlist?list=PLKXe1HzhulvM7IuvwKMp_odaqg7VjFvJ5" # input("Enter video URL: ")


def main(link = yt_url):
    try:
        # # Check if the link is a youtube link / link type
        # ck_link = link_utils.LinkType(link)
        # if ck_link == "NL" :
        #     print(f"Not a youtube link {ck_link}, try again ? ")
        #     retry = str(input("(Y)es,(N)o or (Q)uit?"))
        #     YN(retry)
        #     main()
        # elif ck_link == "VP" or "RD" or "UL":
        #     pass
        # Get the video information
        option = Options(mode=2, playlist=True, debug=False)
        info = yt_utils.Info(url=link, option=option)
        # print(info)
        for inf in range(0, len(info)):
            print(info[inf])
            inf +=1
        
        # print(f"Video Title: {info.get('video_title')},\nWebpage URL: {info.get('webpage_url')},\nDuration: {(info.get('duration')/60)}s\nAudio URL: {info.get('sound_url')},\n")
    except Exception as e:
        print(f"Error: {e}")


# def YN(ans):
#     # str(input("(Y)es,(N)o or (Q)uit?"))
#     if ans.lower() == "y":
#         return True
#     elif ans.lower() == "n":
#         return False
#     elif ans.lower() == "q":
#         exit()
#     else:
#         YN()


if __name__ == '__main__':
    main(link=yt_url)
