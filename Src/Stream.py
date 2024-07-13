import yt_dlp
import os

class Stream:
     def __init__(self, dlf):
          
          self.options = {
               'format': 'bestaudio/best',
               'outtmpl': os.path.join(dlf, '%(title)s.%(ext)s'),
               'abort_on_unavailable_fragments': True,
               'quiet': True,
               'progress': True,
               'no_warnings': True,
               'ignoreerrors': True,
               'keepvideo': False,
               'noplaylist': True,
          }
          
     
     def stream_link(url):
          with yt_dlp.YoutubeDL(options) as ydl:
               info_dict = ydl.extract_info(url, download=False)
               surl = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])
          return surl
     
print(Stream.stream_link(None, "https://www.youtube.com/watch?v=feA64wXhbjo"))