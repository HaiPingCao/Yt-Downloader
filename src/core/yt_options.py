import os

options:dict = {
'format': 'bestaudio/best',
    'no_warnings': True,
    'ignoreerrors': True,
    'quiet': True,
    'verbose': False,
    'simulate': True,
    
    'formats': 'bestaudio/best', 
    'audioformat': 'best',   

    'abort_on_unavailable_fragments': True,
    'keepvideo': False,

    'flat_list': False,
    'noplaylist': False,
}

def Options(
    mode:int, 
    playlist:bool, 
    debug:bool, 
    download_folder:str = "\\Temp",
    playlist_items_index:str = "1-20"
    ):

    '''
    mode:int (1: download mp3, 2: info)\n
    playlist:boolean\n
    debug:boolean \n
    download_folder:str\n
    playlist_items_index:str (default: "1-20", set to "" for full playlist)\n
    '''
    modified_options = options.copy()
    # PLAYLIST ?
    if playlist == False:
        modified_options.update({
            # 'flat_list': True,
            'noplaylist': True
            })
    # DEBUG ?
    if debug == True:
        modified_options.update({
            'no_warnings': False,
            'quiet': False,
            'verbose': True
        })
    #MP3 STREAM / INFO
    if mode == 1:
        pass
    
    # MP3 DOWNLOAD
    elif mode == 2:
        modified_options['simulate'] = False
        modified_options['outtmpl'] = os.path.join(download_folder, '%(title)s.%(ext)s')
        modified_options['postprocessors']=[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
    # PLAYLIST ITEMS INDEX
    if playlist_items_index != "":
        modified_options['playlist_items'] = playlist_items_index

    return modified_options