from abc import ABC, abstractmethod
from app.providers.types import SongOption
from typing import List

'''
Base class for SongDetailsProvider.
'''

class SongDetailsProvider(ABC):
    @abstractmethod
    def get_lyrics(self, song_name: str, song_artist: str):
        pass

    @abstractmethod
    def get_description(self, song_name: str, song_artist: str):
        pass

    @abstractmethod
    def get_all_lyrics(self, songs: List[SongOption]):
        pass

    @abstractmethod
    def get_all_descriptions(self, songs: List[SongOption]):
        pass