from abc import ABC, abstractmethod
from typing import List

'''
Base class for getSongs.
'''

class GetSongOptionsProvider(ABC):
    @abstractmethod
    def get_songs(self, prompt: str, num_songs: int, song_options: List[str]):
        pass