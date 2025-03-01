import random

class Queue(list):
     now_playing = -1
     loop = 0

     # loop = 0: No loop
     # loop = 1: Loop one
     # loop = 2: Loop all

     def __init__(self):
          pass

     def queue(self):
          '''
          https://claude.ai/share/1272d7bc-5da7-489f-902d-278a8a338982
          self[self.nowplaying:] returns a new list containing all items from the current playing position to the end of the queue.
          For example, if:
               The queue contains ["Song A", "Song B", "Song C", "Song D", "Song E"]
               self.nowplaying is 2 (pointing to "Song C")
               Then self[self.nowplaying:] would return ["Song C", "Song D", "Song E"].
               This is used in the queue() method to show the user what songs are coming up next in the playlist.
          '''
          if self.loop == 0:
               og = self[self.now_playing:] # Ongoing queue
               if self.now_playing > 0:
                    og += self[:self.now_playing]
               return og
          return self[self.now_playing:]

     def add(self, song): 
          nsong = self.extend()
          return nsong

     def nowplaying(self):
          return self[self.now_playing]

     def suffle(self):
          '''
          new queue = current song list(currentsong+1)
          random new queue
          current song list(currentsong+1) = new queue
          '''
          new_queue = self[self.now_playing+1:]
          random.shuffle(new_queue)
          self[self.now_playing+1:] = new_queue

     def previous(self):
          if self.loop == 1:
               '''
               If loop 1 track is playing, return the current track.
               '''
               return self[self.now_playing]
          elif self.loop == 2:
               '''
               If loop 2 track is playing, return the next previous track.
               '''
               if self.now_playing == 0:
                    self.now_playing = len(self) - 2
                    return self[len(self) - 1]
               self.now_playing -= 2
               return self[self.now_playing + 1]
          else:
               self.now_playing -= 2
               if self.now_playing+1 >= 0:
                    return self[self.now_playing+1]
               else:
                    self.now_playing += 2

     def __next__(self):
          self.now_playing += 1
          if self.loop == 1:
               if self.now_playing  != 0:
                    self.now_playing -=1
          elif self.loop == 2:
               if self.now_playing == len(self):
                    self.now_playing = 0
          if self.now_playing >= len(self):
               self.now_playing = len(self) - 1
               return None
          return self[self.now_playing]