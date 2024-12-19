from core import utilities as ult
# import re

tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/watch?v=nEoAFBwbYzw" # input("Enter video URL: ")

if __name__ == '__main__':
    # GET VIDEO INFO
    linktype = ult.LinkType(video_url)
    '''
    1: Radio Playlist 
    2: Video with Playlist 
    3: Normal video link 
    4: User-created Playlist 
    0: Unknown or Unsupported YouTube Link 
    ''' 
    if linktype == 1:
        exit("Non youtube link is not supported yet")
    else:
        video_info = ult.Info(video_url)
        print(video_info[0], video_info[1], video_info[2], video_info[3], video_info[4])



# '''queue: link-> check if it's a playlist -> get radio id -> add to queue (radio id + 1 if end start from 0 to start id / end)'''