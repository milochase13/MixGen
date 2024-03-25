from abc import ABC, abstractmethod
from app.providers.types import SongOption
from typing import List

'''
Base class for SongDetailsProvider.
'''

class VDBIngestionProvider(ABC):
    @abstractmethod
    def ingest_lyrics(self, chunks: List[str], metadata):
        pass
