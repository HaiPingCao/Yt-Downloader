import yt_dlp
import os
os.add_dll_directory(r'C:\VLC')
import vlc
import time

class Stream:
     def __init__(self, quiet=None):
          if quiet is None:
               quiet = True
               
          self.options = {
               'format': 'bestaudio/best',
               'abort_on_unavailable_fragments': True,
               'quiet': quiet,
               'progress': True,
               'no_warnings': True,
               'ignoreerrors': True,
               'keepvideo': False,
               'noplaylist': True,
          }
          
     
     def stream_link(self, url):
          try:
               with yt_dlp.YoutubeDL(self.options) as ydl:
                    info_dict = ydl.extract_info(url, download=False)

                    if 'requested_formats' not in info_dict:
                         return "Requested formats not found in the info_dict."

                    # Print available formats
                    available_formats = [f['ext'] for f in info_dict['requested_formats']]
                    print(f"Available formats: {available_formats}")

                    # Attempt to find a suitable format
                    surl = next((f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm']), None)

                    if surl is None:
                         return "Suitable format not found. Available formats are: " + ", ".join(available_formats)

               return surl
          except Exception as e:
               return f"Error: {e}"
     
     def Media_Player(self, url):
          Instance = vlc.Instance()
          player = Instance.media_player_new()
          Media = Instance.media_new(url)
          Media.get_mrl()
          player.set_media(Media)
          player.play()
          time.sleep(100)
     
     
     
link:str = Stream().stream_link("https://www.youtube.com/watch?v=feA64wXhbjo")
print(link)