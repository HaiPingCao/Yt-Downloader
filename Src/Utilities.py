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
        surl = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])
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

    
    
class MediaPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def open_media(self, media_path):
        """Opens a local file or a stream URL."""
        media = self.instance.media_new(media_path)
        self.player.set_media(media)
        self.player.play()

    def music_controls(self, command):
        """Controls the playback of the media."""
        if command == "play":
            self.player.play()
        elif command == "pause":
            self.player.pause()
        elif command == "stop":
            self.player.stop()

    def set_volume(self, volume):
        """Sets the volume (0-100)."""
        self.player.audio_set_volume(volume)

    def get_volume(self):
        """Gets the current volume."""
        return self.player.audio_get_volume()

    def set_position(self, position):
        """Sets the position (0.0 to 1.0)."""
        self.player.set_position(position)

    def get_position(self):
        """Gets the current position (0.0 to 1.0)."""
        return self.player.get_position()

    def get_length(self):
        """Gets the length of the media in milliseconds."""
        return self.player.get_length()

    def get_time(self):
        """Gets the current playback time in milliseconds."""
        return self.player.get_time()

    def set_time(self, time_ms):
        """Sets the current playback time in milliseconds."""
        self.player.set_time(time_ms)

    def is_playing(self):
        """Checks if the media is playing."""
        return self.player.is_playing()

    def get_state(self):
        """Gets the current state of the player."""
        return self.player.get_state()
        
def ST():
    video_url: str =  "https://www.youtube.com/watch?v=0dhSm2n7Gc8" # input("Url: ")
    info: list = Info(video_url)
    player = MediaPlayer()
    player.open_media(info[3])
    
    time.sleep(1)
    print("Controls: play, pause, stop, volume, seek, exit")
    while True:
        command = input("Enter command: ").strip().lower()
        
        if command == "play":
            player.music_controls("play")
        elif command == "pause":
            player.music_controls("pause")
        elif command == "stop":
            player.music_controls("stop")
        elif command.startswith("volume"):
            try:
                volume = int(command.split()[1])
                player.set_volume(volume)
                print(f"Volume set to {volume}")
            except:
                print("Invalid volume command. Use 'volume <value>' where value is between 0 and 100.")
        elif command.startswith("seek"):
            try:
                position = float(command.split()[1])
                player.set_position(position)
                print(f"Seeked to position {position}")
            except:
                print("Invalid seek command. Use 'seek <value>' where value is between 0.0 and 1.0.")
        elif command == "exit":
            player.stop()
            break
        else:
            print("Unknown command. Available commands: play, pause, stop, volume, seek, exit")
        
if __name__ == '__main__':
    
    print(Info('https://www.youtube.com/watch?v=7eoPEWcd_RY')[3])
    