import spotipy
from spotipy.oauth2 import SpotifyOAuth

# spotipy instance
scope = ["user-library-read","playlist-modify-private"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))