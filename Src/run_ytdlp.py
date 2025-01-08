from core import yt_utils, link_utils
from core.options import Options
import yt_dlp
# import re

tempf_path: str = "\\Temp"
yt_url: str = "https://www.youtube.com/watch?v=mQ1ycOl48Hc" # input("Enter video URL: ")


def main(link = yt_url):
    try:
        # Check if the link is a youtube link / link type
        ck_link = link_utils.LinkType(link)
        if ck_link == "NL" :
            print(f"Not a youtube link {ck_link}, try again ? ")
            retry = str(input("(Y)es,(N)o or (Q)uit?"))
            YN(retry)
            main()
        elif ck_link == "VP" or "RD" or "UL":
            pass
        # Get the video information
        option = Options(mode=2, playlist=True, debug=True)
        info = yt_utils.Info(url=link, option=option)
        print(f"Video Title: {info[0]},\nWebpage URL: {info[1]},\nDuration: {info[2]}\nAudio URL: {info[3]},\n")
    except Exception as e:
        print(f"Error: {e}")



def YN(ans):
    # str(input("(Y)es,(N)o or (Q)uit?"))
    if ans.lower() == "y":
        return True
    elif ans.lower() == "n":
        return False
    elif ans.lower() == "q":
        exit()
    else:
        YN()



if __name__ == '__main__':
    main(link=yt_url)
