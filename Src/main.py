import Utilities
import os
import vlc
import time


tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/watch?v=DZ0oir_DLao" #input("Enter video URL: ")


if __name__ == '__main__':
     X = Utilities.Info(video_url)
     
     for i in X:
          print(i)
     print('\n//////////////////////////\n')
     
     # Utilities.Media_Player(X[3], X[2])
     # Utilities.Media_Player("\\Temp\\BEAUZ - Outerspace (feat. Dallas) [Monstercat Release].m4a", 1000)
     # Utilities.Yt_downloader(video_url, tempf_path)
     