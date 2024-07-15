import Stream
import os
os.add_dll_directory(r'C:\VLC')
import vlc
import time


tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/watch?v=0dhSm2n7Gc8&list=RD0dhSm2n7Gc8&start_radio=1" #input("Enter video URL: ")


def I4T(link: str):
     X = Stream.Info(link)
     A = X[0]
     B = X[1]
     C = X[2]
     D = X[3]
     return A, B, C, D


# def main(link: str):
#      I4T(link)


if __name__ == '__main__':
     # print(main(video_url))
     print(I4T(video_url))
     print('//////////////////////////\n')
     
     Stream.Media_Player(I4T(video_url)[3], I4T(video_url)[2])