import yt_dlp
import os

def Info(url):
    i4o = {
        'no_warnings': True,
        'ignoreerrors': True,
        'abort_on_unavailable_fragments': True,
        'flat_list': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(i4o) as info:
        info_dict = info.extract_info(url, download=False)
        
        video_id = info_dict.get('id', None)
        video_title = info_dict.get('title', None)
        webpage_url = info_dict.get('webpage_url', None)
        surl = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])
    return video_id, video_title, webpage_url, surl

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
    
print(Info("https://www.youtube.com/watch?v=0dhSm2n7Gc8")[0])