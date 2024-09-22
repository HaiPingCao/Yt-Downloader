import os

options:dict = {
'format': 'bestaudio/best',
    'no_warnings': True,
    'ignoreerrors': True,
    'quiet': True,
    'verbose': False,

    'abort_on_unavailable_fragments': True,
    'keepvideo': False,

    'flat_list': False,
    'noplaylist': False,
}

def opts(mode:int, playlist:bool, debug:bool, download_folder:str = "\\Temp"):
    '''mode [1/2] - playlist [True/False] - debug [True/False] - download_folder [str]'''
    modified_options = options.copy()
    # PLAYLIST ?
    if playlist == False:
        modified_options.update({
            'flat_list': True,
            'noplaylist': True
            })
    # DEBUG ?
    if debug == True:
        modified_options.update({
            'no_warnings': False,
            'quiet': False,
            'verbose': True
        })
    # MP3 DOWNLOAD
    if mode == 1:
        modified_options['outtmpl'] = os.path.join(download_folder, '%(title)s.%(ext)s')
        modified_options['postprocessors']=[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
    #MP3 STREAM / INFO
    elif mode == 2:
        pass

    return modified_options