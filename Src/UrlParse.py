from urllib.parse import urlparse, parse_qs

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

print(url_parse('https://www.youtube.com/watch?v=gGrVAfna1fo&list=RDgGrVAfna1fo&start_radio=1'))
print(url_parse('https://www.youtube.com/watch?v=ALZHF5UqnU4&list=PLKXe1HzhulvPr_TbyHJYJ9OR5KbNRpgVK&pp=gAQBiAQB'))
print(url_parse('https://www.youtube.com/watch?v=0Kw8QqQHq24'))
print(url_parse('https://www.youtube.com/playlist?list=PLKXe1HzhulvPr_TbyHJYJ9OR5KbNRpgVK'))