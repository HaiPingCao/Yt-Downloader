import utilities as ult


# class queue(list):
#      def __init__(self):
#           super().__init__()

#      def add(self, url):
#           self.append(url)
#           ult.DL(url, ult.tempf_path, playlist=False)
          
if __name__ == '__main__':
     url = "https://www.youtube.com/watch?v=gGrVAfna1fo&list=RDOJBxNA8cX-E&index=3"
     parse = ult.LinkType(url)
     print(parse)
     '''
     1: Radio Playlist 
     2: Video with Playlist 
     3: Normal video link 
     4: User-created Playlist 
     0: Unknown or Unsupported YouTube Link 
     '''
     