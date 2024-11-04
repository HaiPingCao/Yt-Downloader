from core import utilities as ult
import re

tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/watch?v=LecuZccoWBs&list=RDGMEMCMFH2exzjBeE_zAHHJOdxgVMLecuZccoWBs&start_radio=1" # input("Enter video URL: ")

if __name__ == '__main__':
    # DOWNLOAD VIDEO
    # ult.DL(video_url, tempf_path, playlist=True)
    
    
    # GET VIDEO INFO
    linktype = ult.LinkType(video_url)
    # print(linktype)
    '''
    1: Radio Playlist 
    2: Video with Playlist 
    3: Normal video link 
    4: User-created Playlist 
    0: Unknown or Unsupported YouTube Link 
    '''
    linkparse = ult.LinkParse(video_url)
    # print(linkparse)
    # print("\n")
    rdn = linkparse[1].get('start_radio', None)
    for i in rdn:
        print(i)

'''queue: link-> check if it's a playlist -> get radio id -> add to queue (radio id + 1 if end start from 0 to start id / end)'''