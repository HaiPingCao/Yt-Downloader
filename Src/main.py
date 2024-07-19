import Utilities


tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/watch?v=DZ0oir_DLao"  #input("Enter video URL: ")

if __name__ == '__main__':
    X = Utilities.Info(video_url)

    for i in X:
        print(i)
    print('\n//////////////////////////\n')

    Utilities.MediaPlayer(X[3], X[2])
    # Utilities.YtDownloader(video_url, tempf_path)
