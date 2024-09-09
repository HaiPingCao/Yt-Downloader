
options:dict = {
     'no_warnings': True,
     'ignoreerrors': True,
     'quiet': True,

     'abort_on_unavailable_fragments': True,
     'keepvideo': False,

     'flat_list': True,
     'noplaylist': True,

     'postprocessors': [
          {
               'key': 'FFmpegExtractAudio',
               'preferredcodec': 'mp3',
               'preferredquality': '192',
          }
     ],
}

def opts(mode:int, playlist:bool):
     m_opts:dict = options.copy()
     if mode == 0 & playlist == False:       #Debug
          m_opts.update({
               'no_warnings': False,
               'ignoreerrors': False,
               'quiet': False
               })
     elif mode == 1 & playlist == False:     #Information - No Playlist
          m_opts.pop('postprocessors')
     elif mode == 1 & playlist == True:      #Information - Playlist
          m_opts.pop('postprocessors')
     elif mode == 2 & playlist == False:     #Music - No Playlist
          m_opts.update({
               'flat_list': True,
               'noplaylist': True
               })
     elif mode == 2 & playlist == True:      #Music - Playlist
          m_opts.update({
               'flat_list': False,
               'noplaylist': False,
               })

     return m_opts

if __name__ == '__main__':
     print(f'\n{options}\n')
     fn = opts(2, True)
     print(fn)
     # moptions = options.copy()
     # print(moptions)