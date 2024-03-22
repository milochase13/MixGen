from abc import ABC, abstractmethod
from typing import List

'''
Base class for getSongs.
'''

class SongDetailsProvider(ABC):
    @abstractmethod
    def get_lyrics(self, song_id: str):
        pass

    @abstractmethod
    def get_description(self, song_id: str):
        pass