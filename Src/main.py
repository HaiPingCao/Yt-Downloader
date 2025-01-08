from core import yt_utils as ult
from core.options import Options
# import re

tempf_path: str = "\\Temp"
yt_url: str = "https://www.outube.com/watch?v=nEoAFBwbYzw" # input("Enter video URL: ")


def ToBeExcute(link = yt_url):
    # Check if the link is a youtube link / link type
    ck_link = ult.LinkType(link)
    if ck_link == "NL" :
        print("Not a youtube link, try again")
        ToBeExcute()
    elif ck_link == "VP" or "RD" or "UL":
        pass
    # Get the video information
    info = ult.Info(link)
    print(f"Video Title: {info[0]},\nWebpage URL: {info[1]},\nDuration: {info[2]}\nAudio URL: {info[3]},\n")


def YN(ans = str(input())):
    if ans.lower() == "y":
        return True
    elif ans.lower() == "n":
        return False
    elif ans.lower() == "q":
        exit()
    else:
        print("(Y)es,(N)o or (Q)uit?")
        YN()


def CustomErrorHandler(dl_path: str = tempf_path, video_url: str = yt_url):
    try:
        ToBeExcute()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    CustomErrorHandler(video_url=yt_url)
