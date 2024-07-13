import downloader
import os
os.add_dll_directory(r'C:\VLC')
import vlc

from downloader import i4o

print(i4o)


tempf_path: str = "\\Temp"
video_url_input: str = input("Enter video URL: ")

if __name__ == '__main__':

     playurl = downloader.Info(video_url_input)[3]     
     downloader.Yt_downloader(playurl, tempf_path)
     
     
     # playurl = downloader.Info(video_url_input)[3]     
     # print(playurl)
     
     # Instance = vlc.Instance()
     # player = Instance.media_player_new()
     # Media = Instance.media_new(playurl)
     # Media.get_mrl()
     # player.set_media(Media)
     # player.play()
     # time.sleep(100)