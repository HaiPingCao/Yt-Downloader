from urllib.parse import urlparse, parse_qs

def LinkParse(url):
     # Parse the URL into its components
     parsed_url = urlparse(url)
     # Get query parameters from the URL
     query_params = parse_qs(parsed_url.query)
     return parsed_url, query_params

def LinkType(url):
     '''
     RD: Radio Playlist 
     VP: Video with Playlist 
     NP: Normal video link 
     UL: User-created Playlist 
     NL: Unknown or Unsupported YouTube Link 
     '''
     parsed = LinkParse(url)
     parsed_url = parsed[0]
     query_params = parsed[1]
     
     if parsed_url.netloc != 'www.youtube.com': return "NL"
     if parsed_url.path == '/watch':
          if 'v' in query_params:
               video_id = query_params['v'][0]
               # Check if the video link has a playlist associated with it
               if 'list' in query_params:
                    playlist_id = query_params['list'][0]
                    # Differentiate between auto-generated (RD) and normal playlists
                    if playlist_id.startswith('RD'):
                         return "RD" # Radio Playlist Link (auto-generated)
                    else:
                         return "VP" # Video with Playlist Link
               else:
                    return "NP" # Normal video link (no playlist)
     # Check if it's a direct playlist link
     if parsed_url.path == '/playlist' and 'list' in query_params:
          return "UL" # User-created Playlist Link


