from app.providers.SongDetailsProviderBase import SongDetailsProvider
from app.providers.types import SongOption
from lyricsgenius import Genius
from typing import List

class SongDetailsProviderGeniusImpl(SongDetailsProvider):

    def __init__(self, access_token):
        self.access_token = access_token
        self.geniusClient = Genius(access_token, timeout=10, sleep_time=0.5)

    def get_song(self, song_name: str, song_artist: str):
        return self.geniusClient.search_song(title=song_name, artist=song_artist, get_full_info=False)
    
    def get_lyrics(self, song_name: str, song_artist: str):
        song = self.get_song(song_name, song_artist)
        if song:
            return song.lyrics
        return None
    
    def get_description(self, song_name: str, song_artist: str):
        song = self.get_song(song_name, song_artist)
        if song:
            return self.geniusClient.song_annotations(song.id)
        return None
    
    def get_all_lyrics(self, songs: List[SongOption]):
        lyrics = {}
        for song in songs:
            lyric = self.get_lyrics(song["song"], song["artist"])
            if lyric:
                lyrics[song["song"]+" by "+song["artist"]] = lyric
        return lyrics
    
    def get_all_descriptions(self, songs: List[SongOption]):
        descriptions = {}
        for song in songs:
            description = self.get_description(song["song"], song["artist"])
            if description:
                descriptions[song["song"]+" by "+song["artist"]] = description
        return descriptions

