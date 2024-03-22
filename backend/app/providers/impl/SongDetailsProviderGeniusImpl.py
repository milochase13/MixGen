from app.providers.SongDetailsProviderBase import SongDetailsProviderBase
from lyricsgenius import Genius

class SongDetailsProviderGeniusImpl(SongDetailsProviderBase):

    def __init__(self, access_token):
        self.access_token = access_token
        self.geniusClient = Genius(access_token)
        self.song = None

    def get_song(self, song_name: str, song_artist: str):
        self.song = self.geniusClient.search_song(title=song_name, artist=song_artist, get_full_info=False)
    
    def get_lyrics(self, song_name: str, song_artist: str):
        if not self.song:
            self.get_song(song_name, song_artist)
        return self.song.lyrics
    
    def get_description(self, song_name: str, song_artist: str):
        if not self.song:
            self.get_song(song_name, song_artist)
        return self.geniusClient.song_annotations(self.song.id)
    
