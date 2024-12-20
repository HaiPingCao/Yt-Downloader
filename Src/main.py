from core import utilities as ult
import re

tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/watch?v=WPl10ZrhCtk&list=RDOIBODIPC_8Y&index=2" # input("Enter video URL: ")

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
