import yt_dlp
import os
# import vlc


def INFO(url):
    i4o = {
        'no_warnings': True,
        'ignoreerrors': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(i4o) as info:
        info_dict = info.extract_info(url, download=False)
        
        video_id = info_dict.get('id', None)
        video_title = info_dict.get('title', None)
        webpage_url = info_dict.get('webpage_url', None)
        url = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])

    return video_id, video_title, webpage_url, url

def YT_DOWNLOADER(video_url, download_folder):

    options = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'quiet': False,
        'progress': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'keepvideo': False,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        entry = INFO(video_url)[2]
        ydl.download(entry)
    
    # with yt_dlp.YoutubeDL(options) as ydl:
    #     info_dict = ydl.extract_info(video_url, download=False)

    #     if 'entries' in info_dict:
    #         # This is a playlist
    #         for entry in info_dict['entries']:
    #             print(f"Downloading: {entry['title']}")
    #             ydl.download([entry['webpage_url']])
    #     else:
    #         # This is a single video
    #         ydl.download([video_url])
        

if __name__ == '__main__':
    tempf_path = "\\Temp"
    video_url_input = str(input("Enter video URL: "))
    print(INFO(video_url_input)[3])
    # if video_url_input.startswith("https://www.youtube.com/playlist?list="):
    #     YT_DOWNLOADER(video_url_input, tempf_path)
    # else:
    #     YT_DOWNLOADER(video_url_input, tempf_path)
