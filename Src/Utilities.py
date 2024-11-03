import yt_dlp
import os
from urllib.parse import urlparse, parse_qs
from options import opts

def Info(url):
    '''
    Return: video_title, webpage_url, duration, s_url
    '''
    with yt_dlp.YoutubeDL(opts(mode=2, playlist=False, debug=True)) as info:
        info_dict = info.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        webpage_url = info_dict.get('webpage_url', None)
        duration = info_dict.get('duration', None)
        s_url = next(
            (f['url'] for f in info_dict['formats'] 
             if f['ext'] in ['m4a', 'webm'] and f.get('vcodec') == 'none'),  # Check that there is no video track
            None  # Default to None if no match is found
        )
        # s_url = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])
    return video_title, webpage_url, duration, s_url, info_dict

def DL(video_url, download_folder, playlist=False):
    with yt_dlp.YoutubeDL(opts(mode=1, playlist=playlist, debug=True, download_folder=download_folder)) as ydl:
        entry = Info(video_url)[1]
        ydl.download(entry)

def url_parse(url):
    '''
    1: Radio Playlist 
    2: Video with Playlist 
    3: Normal video link 
    4: User-created Playlist 
    0: Unknown or Unsupported YouTube Link 
    '''
    # Parse the URL into its components
    parsed_url = urlparse(url)
    # Get query parameters from the URL
    query_params = parse_qs(parsed_url.query)
    # Check if it's a "watch" URL (normal video link or video with playlist)
    if parsed_url.path == '/watch':
        if 'v' in query_params:
            video_id = query_params['v'][0]
            
            # Check if the video link has a playlist associated with it
            if 'list' in query_params:
                playlist_id = query_params['list'][0]
                
                # Differentiate between auto-generated (RD) and normal playlists
                if playlist_id.startswith('RD'):
                        return 1 # Radio Playlist Link (auto-generated)
                else:
                        return 2 # Video with Playlist Link
            else:
                return 3 # Normal video link (no playlist)
    # Check if it's a direct playlist link
    elif parsed_url.path == '/playlist' and 'list' in query_params:
        return 4 # User-created Playlist Link
    # If it doesn't match any known YouTube link pattern
    return 0 # 'Unknown or Unsupported YouTube Link'
        
if __name__ == '__main__':
    
    print(Info('https://www.youtube.com/watch?v=ECn51ZLTdAQ')[3])
    # print(opts(mode=1, playlist=False, debug=False, download_folder="C:\\Temp"))