import Utilities
import os

import vlc
import time


tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/watch?v=DZ0oir_DLao" #input("Enter video URL: ")


def I4T(link: str):
     X = Utilities.Info(link)
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
     
     Utilities.Media_Player(I4T(video_url)[3], I4T(video_url)[2])