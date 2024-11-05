from core import utilities as ult

class queue(list):
     def __init__(self):
          super().__init__()

     def add(self, url):
          self.append(url)
     
          ult.DL(url, ult.tempf_path, playlist=False)
          
