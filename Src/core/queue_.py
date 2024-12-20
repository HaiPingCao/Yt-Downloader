# from core import utilities as ult
import random
import utilities as ult

lst = []

# class MusicQueue(list):
#      nowplaying = -1
#      loop = 0
     
     
#      def __init__(self):
#           pass

#      def queue(self):
#           if self.loop == 2:
#                og_queue = self[self.nowplaying:]
#                if self.nowplaying > 0:
#                     og_queue += self[:self.nowplaying]
#                return og_queue
#           return self[self.nowplaying:]

#      def add_queue(self, data):
#           # rdata = self.extend([QueueData(i) for i in data])
#           rdata = self.extend([lst[i] for i in data])
#           return rdata

#      def now_playing(self):
#           return self[self.nowplaying]

#      def shuffle(self):
#           new_list = self[self.nowplaying+1:]
#           random.shuffle(new_list)
#           self[self.nowplaying+1:] = new_list

#      def prev(self):
#           if self.loop == 1:
#                return self[self.nowplaying]
#           elif self.loop == 2:
#                if self.nowplaying == 0:
#                     self.nowplaying = len(self) - 2
#                     return self[len(self)-1]
#                self.nowplaying -= 2
#                return self[self.nowplaying+1]
#           else:
#                self.nowplaying -= 2
#                if self.nowplaying+1 >= 0:
#                     return self[self.nowplaying+1]
#                else:
#                     self.nowplaying += 2

#      def __next__(self):
#           self.nowplaying += 1
#           if self.loop == 1:
#                if self.nowplaying != 0:
#                     self.nowplaying -= 1
#           elif self.loop == 2:
#                if self.nowplaying == len(self):
#                     self.nowplaying = 0
#           if self.nowplaying >= len(self):
#                self.nowplaying = len(self)-1
#                return None
#           return self[self.nowplaying] + self[self.nowplaying+1] + self[self.nowplaying+2]

# queue = MusicQueue()
# queue.append("-sdsda")
# queue.append("-dhjts")
# queue.append("-bbcxc")

# print("#### - ",queue)
# print(queue.shuffle())
# print("#### - ",queue)
# print(queue.prev())
# print("#### - ",queue)
# print(queue.__next__())
# print("#### - ",queue)
# # print(queue.add_queue("123456"))
# # print(queue.nowplaying())

def RadioPlaylist(video_url):
     LinkParse = ult.LinkParse(video_url)
     try:
          rdn = LinkParse[1].get('start_radio', None) or LinkParse[1].get('index', None)
          for i in rdn:
               return i
     except Exception as e:
          return None