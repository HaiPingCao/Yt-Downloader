from core import utilities as ult
from core import options as opts
import re

tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/watch?v=sJXZ9Dok7u8&list=RDEug-A577g-U&index=3" # input("Enter video URL: ")

if __name__ == '__main__':
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
    
    if linktype == 1:
        exit("Non youtube link is not supported yet")
    
    def RadioPlaylist(video_url):
        LinkParse = ult.LinkParse(video_url)
        try:
            rdn = LinkParse[1].get('start_radio', None) or LinkParse[1].get('index', None)
            for i in rdn:
                print(i)
                
        except Exception as e:
            print("Error: ", e)




'''queue: link-> check if it's a playlist -> get radio id -> add to queue (radio id + 1 if end start from 0 to start id / end)'''