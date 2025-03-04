import yt_dlp
from core.options import Options


def Info(url, option=Options(mode=2, playlist=False, debug=False)):
    '''
    return: video_title, webpage_url, duration, s_url, info_dict
    '''
    try:
        with yt_dlp.YoutubeDL(option) as info:
            info_dict = info.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            webpage_url = info_dict.get('webpage_url', None)
            duration = info_dict.get('duration', None)
            s_url = next(
                (f['url'] for f in info_dict['formats'] 
                    if f['ext'] in ['m4a', 'webm'] and f.get('vcodec') == 'none'),  # Check that there is no video track
                # None  # Default to None if no match is found
            )
            
            if "entries" in info_dict:
                print(f"==========>{info_dict["entries"][0]}")
            #     for entry in info_dict["entries"]:
            #         print(entry)
            
            # '''
            # # Loop through all available formats
            # for format in info_dict['formats']:
            #     # Check if this is an audio-only m4a or webm format
            #     is_audio_format = format['ext'] in ['m4a', 'webm']
            #     is_audio_only = format.get('vcodec') == 'none'
                
            #     # If we found an audio-only format we want
            #     if is_audio_format and is_audio_only:
            #         # Return its URL
            #         audio_url = format['url']
            #         break
            # '''
    except yt_dlp.utils.DownloadError as e:
        print(f"Error extracting info: {e}")
        return {
            'video_title': None, 
            'webpage_url': None, 
            'duration': None, 
            'sound_url': None, 
            'full_info': None
            }

    return {
        'video_title': video_title, 
        'webpage_url': webpage_url, 
        'duration': duration, 
        'sound_url': s_url, 
        'full_info': info_dict
        }


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
