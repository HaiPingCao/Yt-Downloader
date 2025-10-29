import yt_dlp
from core.options import Options
from yt_dlp.utils import DownloadError


def Info(url, option=Options(mode=2, playlist=False, debug=False)):
    '''
    return: video_title, webpage_url, duration, sound_url, info_dict
    '''
    try:
        with yt_dlp.YoutubeDL(option) as info:
            info_dict = info.extract_info(url, download=False)
            return_list = []
            
            entries = info_dict.get('entries', [info_dict])
            
            for entry in entries:
                video_title = entry.get('title', None)
                webpage_url = entry.get('webpage_url', None)
                duration = entry.get('duration', None)
                sound = None
                if entry and 'formats' in entry and entry['formats']:
                    sound = next(
                        (f['url'] for f in entry['formats']
                         if f and 'ext' in f and 'url' in f and f['ext'] in ['m4a', 'webm'] and f.get('vcodec') == 'none'),
                        None
                    )
                return_list.append((video_title, webpage_url, duration, sound))
            
            return return_list

    except DownloadError as e:
        print(f"Error extracting info: {e}")
        return []


# def Download(video_url, download_folder, playlist=False):
#     with yt_dlp.YoutubeDL(
#         Options(
#             mode=1,
#             playlist=playlist, 
#             debug=True, 
#             download_folder=download_folder
#             )) as ydl:
#         entry = Info(video_url)[1]
#         ydl.download(entry)
