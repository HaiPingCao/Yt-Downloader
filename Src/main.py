import Utilities


tempf_path: str = "\\Temp"
video_url: str = input("Enter video URL: ")

if __name__ == '__main__':
    X = Utilities.Info(video_url)

    for i in X:
        print(i)
    print('\n//////////////////////////\n')



