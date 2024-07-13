import yt_dlp
import os

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
          with yt_dlp.YoutubeDL(self.options) as ydl:
               info_dict = ydl.extract_info(url, download=False)
               
               # if 'requested_formats' not in info_dict:
               #      return "Suitable format not found."
               # else:
               surl = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])
          return surl
     
     
link:str = Stream().stream_link("https://www.youtube.com/watch?v=feA64wXhbjo")
print(link)