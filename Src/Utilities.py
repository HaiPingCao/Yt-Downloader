import yt_dlp
import time
import os

vlc: str = '../VLC_Win'
os.add_dll_directory(os.getcwd())  # os.add_dll_directory(vlc)  # os.add_dll_directory(os.getcwd())  # os.add_dll_directory(r'C:\VLC')
import vlc


def Info(url):
    i4o = {
        'no_warnings': True,
        'ignoreerrors': True,
        'abort_on_unavailable_fragments': True,
        'flat_list': True,
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(i4o) as info:
        info_dict = info.extract_info(url, download=False)

        video_title = info_dict.get('title', None)
        webpage_url = info_dict.get('webpage_url', None)
        duration = info_dict.get('duration', None)

        surl = next(f['url'] for f in info_dict['requested_formats'] if f['ext'] in ['m4a', 'webm'])
    return video_title, webpage_url, duration, surl


def YtDownloader(video_url, download_folder):
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


# def MediaPlayer(url, duration):
#     Instance = vlc.Instance()
#     player = Instance.media_player_new()
#     Media = Instance.media_new(url)
#     Media.get_mrl()
#     player.set_media(Media)
#     player.play()
#     time.sleep(duration)
    
    
class MediaPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def open_media(self, media_path):
        """Opens a local file or a stream URL."""
        media = self.instance.media_new(media_path)
        self.player.set_media(media)
        self.player.play()

    def play(self):
        """Plays the media."""
        self.player.play()

    def pause(self):
        """Pauses the media."""
        self.player.pause()

    def stop(self):
        """Stops the media."""
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
        
        
        
if __name__ == '__main__':
    video_url: str = "https://rr1---sn-8qj-i5ozr.googlevideo.com/videoplayback?expire=1721391003&ei=OwOaZp7yOPyWvcAPh97T8Aw&ip=113.190.214.224&id=o-AMCib8zvbXvPm96Xr6KodQ5BaESLcT-yQGzbjTjVVONt&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&mh=08&mm=31%2C29&mn=sn-8qj-i5ozr%2Csn-8qj-i5oks&ms=au%2Crdu&mv=m&mvi=1&pl=25&gcr=vn&initcwndbps=1763750&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=2642829&dur=163.199&lmt=1609958598735730&mt=1721369084&fvip=1&keepalive=yes&c=IOS&txp=2311222&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cgcr%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRQIhAIVqU3jaUE8AtyhRY5YqBP9o0JRnV67yaqDY8aoZ2Il9AiB-fM3V5bKbJiglxn5OhlFtcGloYLulngDAiEpyTuaO5w%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AHlkHjAwRQIhAJeExYnxB-9byEkKu_HPsIkVWDQO1uCrvatuhZ73QlLBAiAk9BXleUksd6VNqdb2oXx9NVIVAkMXqQfIXk3x8H_EQw%3D%3D"
    # info: list = Info(video_url)
    player = MediaPlayer()
    player.open_media(video_url)
    
    time.sleep(1)
    print("Controls: play, pause, stop, volume, seek, exit")
    while True:
        command = input("Enter command: ").strip().lower()
        
        if command == "play":
            player.play()
        elif command == "pause":
            player.pause()
        elif command == "stop":
            player.stop()
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