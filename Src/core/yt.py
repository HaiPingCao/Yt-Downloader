import yt_dlp
from core.options import Options


def Info(url, option=Options(mode=2, playlist=False, debug=False)):
    '''
    return: video_title, webpage_url, duration, s_url, info_dict
    '''
    try:
        with yt_dlp.YoutubeDL(option) as info:
            info_dict = info.extract_info(url, download=False)
            return_list = []
            
            if 'entries' not in info_dict or not info_dict['entries']:
                video_title = info_dict.get('title', None)
                webpage_url = info_dict.get('webpage_url', None)
                duration = info_dict.get('duration', None)
                sound = next(
                    (f['url'] for f in info_dict['formats'] 
                        if f['ext'] in ['m4a', 'webm'] and f.get('vcodec') == 'none'),  # Check that there is no video track
                    None  # Default to None if no match is found
                )
                return_list.append((video_title, webpage_url, duration, sound))
                return return_list
            
            for entry in info_dict['entries']:
                video_title = entry.get('title', None)
                webpage_url = entry.get('webpage_url', None)
                duration = entry.get('duration', None)
                sound = next(
                    (f['url'] for f in entry['formats'] 
                        if f['ext'] in ['m4a', 'webm'] and f.get('vcodec') == 'none'),
                    None 
                )
                return_list.append((video_title, webpage_url, duration, sound))
            return return_list
            # return video_title, webpage_url, duration, sound
                    
   


    except yt_dlp.utils.DownloadError as e:
        print(f"Error extracting info: {e}")
        return None


def Download(video_url, download_folder, playlist=False):
    with yt_dlp.YoutubeDL(
        Options(
            mode=1,
            playlist=playlist, 
            debug=True, 
            download_folder=download_folder
            )) as ydl:
        entry = Info(video_url)[1]
        ydl.download(entry)
