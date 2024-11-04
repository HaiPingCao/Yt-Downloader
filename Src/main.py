import core.utilities as utilities

tempf_path: str = "\\Temp"
video_url: str = "https://www.youtube.com/playlist?list=PLKXe1HzhulvPr_TbyHJYJ9OR5KbNRpgVK" # input("Enter video URL: ")

if __name__ == '__main__':
    utilities.DL(video_url, tempf_path, playlist=True)



