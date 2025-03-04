import random

class Queue(list):
    now_playing = -1
    loop = 0  # 0: No loop, 1: Loop one, 2: Loop all

    def queue(self):
        """
        Returns the remaining queue based on current loop mode.
        
        If loop is 0 (No loop):
        - Returns remaining tracks from current position
        - If not at the start, appends tracks from the beginning
        
        If loop is 1 or 2:
        - Returns remaining tracks from current position
        """
        if self.loop == 0:
            og = self[self.now_playing:]
            if self.now_playing > 0:
                og += self[:self.now_playing]
            return og
        return self[self.now_playing:]

    def add(self, song):
        """
        Add song(s) to the queue.
        
        Args:
            song (str or list): A single song or list of songs to add
        
        Returns:
            list: Added songs
        """
        # Convert single song to list if needed
        songs_to_add = song if isinstance(song, list) else [song]
        
        # Extend the queue
        self.extend(songs_to_add)
        
        return songs_to_add

    def nowplaying(self):
        """
        Returns the currently playing track.
        
        Returns:
            The track at the current now_playing index
        """
        return self[self.now_playing]

    def shuffle(self):
        """
        Shuffles the queue from the next track onwards.
        Keeps the current track and previous tracks in order.
        """
        new_queue = self[self.now_playing+1:]
        random.shuffle(new_queue)
        self[self.now_playing+1:] = new_queue

    def previous(self):
        """
        Move to the previous track based on loop mode.
        
        Loop mode 0 (No loop): 
        - Moves back, prevents going before the start
        
        Loop mode 1 (Single track):
        - Returns current track
        
        Loop mode 2 (Loop all):
        - Wraps around to the end of the playlist if at the start
        """
        if self.loop == 1:
            return self[self.now_playing]
        
        elif self.loop == 2:
            if self.now_playing == 0:
                self.now_playing = len(self) - 2
                return self[len(self) - 1]
            
            self.now_playing -= 2
            return self[self.now_playing + 1]
        
        else:
            self.now_playing -= 2
            
            if self.now_playing + 1 >= 0:
                return self[self.now_playing + 1]
            else:
                self.now_playing += 2

    def next(self):
        """
        Move to the next track based on loop mode.
        
        Returns:
            Next track or None if no more tracks
        """
        self.now_playing += 1

        if self.loop == 1:
            # Stay on the same track
            if self.now_playing != 0:
                self.now_playing -= 1

        elif self.loop == 2:
            # Wrap around to start if reached end
            if self.now_playing == len(self):
                self.now_playing = 0

        # Prevent going beyond list length
        if self.now_playing >= len(self):
            self.now_playing = len(self) - 1
            return None

        return self[self.now_playing]
