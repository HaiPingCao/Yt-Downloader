import os
import spotify_dl

def download_playlist(playlist_link, output_dir):
    # Download the playlist
    spotify_dl.download(playlist_link, output_dir)

if __name__ == "__main__":
    playlist_link = input("Enter Spotify playlist link: ")
    output_dir = input("Enter output directory: ")

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download the playlist
    download_playlist(playlist_link, output_dir)
