import subprocess
import yt_dlp
from core.yt_options import Options
from yt_dlp.utils import DownloadError


async def extract_info(
    url, 
    option=Options(mode=2, playlist=False, debug=False), 
    # write_json:bool=False
    ):
    '''
    return: video_title, webpage_url, duration, sound_url, info_dict
    '''
    try:
        with yt_dlp.YoutubeDL(option) as info:
            info_dict = info.extract_info(url, download=False)
            return_list = []
            
            entries = info_dict.get('entries', [info_dict])
            for entry in entries:
                # print(entry)
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
                # if write_json:
                #     with open("info_list.json", "w") as f:
                #         json.dump(info_dict, f, indent=4)
                return_list.append((video_title, webpage_url, duration, sound))
            
            return return_list

    except DownloadError as e:
        print(f"Error extracting info: {e}")
        return []


def get_playlist_count(url):
    result = subprocess.run([
        'yt-dlp',
        '--flat-playlist',
        '--print', '%(playlist_count)s',
        '--playlist-items', '1',  # Only process first item
        url
    ], capture_output=True, text=True)
    
    return int(result.stdout.strip())