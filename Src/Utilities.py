import yt_dlp
import time
import os

dir: str = os.getcwd()
os.add_dll_directory(dir)
import vlc


def Info(url):
    '''
    Returns: video_title, webpage_url, duration, surl
    '''
    i4o = {
        'no_warnings': True,
        'ignoreerrors': True,
        'abort_on_unavailable_fragments': True,
        'flat_list': True,
        'noplaylist': True,
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(i4o) as info:
        info_dict = info.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        webpage_url = info_dict.get('webpage_url', None)
        duration = info_dict.get('duration', None)
        surl = next(
            (f['url'] for f in info_dict['requested_formats'] 
             if f['ext'] in ['m4a', 'webm'] and f.get('vcodec') == 'none'),  # Check that there is no video track
            None  # Default to None if no match is found
        )
        # surl = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])
    return video_title, webpage_url, duration, surl, info_dict

def DL(video_url, download_folder):
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
        entry = Info(video_url)[1]
        ydl.download(entry)

        
if __name__ == '__main__':
    
    print(Info('https://www.youtube.com/watch?v=7eoPEWcd_RY')[3])
    