import yt_dlp
import os
os.add_dll_directory(r'C:\VLC')
import vlc
import time



def Info(url):
     i4o = {
          'no_warnings': True,
          'ignoreerrors': True,
          'abort_on_unavailable_fragments': True,
          'flat_list': True,
          'noplaylist': True,
          'quiet': True,
     }
     with yt_dlp.YoutubeDL(i4o) as info:
          info_dict = info.extract_info(url, download=False)
          
          video_title = info_dict.get('title', None)
          webpage_url = info_dict.get('webpage_url', None)
          duration = info_dict.get('duration', None)
          
          surl = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])
     return video_title, webpage_url, duration, surl


# def stream_link(self, url):
#      try:
#           with yt_dlp.YoutubeDL(self.options) as ydl:
#                info_dict = ydl.extract_info(url, download=False)
#                requested_formats = info_dict.get('requested_formats', [])
#                surl = next((f['url'] for f in requested_formats if f['ext'] in ['m4a', 'webm']), None)
#      except Exception as e:
#           return "Error occurred: {}".format(str(e))
     
#      if surl is None:
#           return "Suitable format not found."
#      else:
#           return surl


def Media_Player(url, duration):
     Instance = vlc.Instance()
     player = Instance.media_player_new()
     Media = Instance.media_new(url)
     Media.get_mrl()
     player.set_media(Media)
     player.play()
     time.sleep(duration)


def Yt_downloader(video_url, download_folder):
     options = {
          'format': 'bestaudio/best',
          'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
          'abort_on_unavailable_fragments': True,
          'quiet': False,
          'progress': True,
          'no_warnings': True,
          'ignoreerrors': True,
          'keepvideo': False,
          'noplaylist': True,
          'postprocessors': [
               {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
               }
          ],
     }
     with yt_dlp.YoutubeDL(options) as ydl:
          entry = Info(video_url)[2]
          ydl.download(entry)


