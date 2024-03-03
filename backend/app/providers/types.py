from typing import TypedDict, List

'''
My own random learning... Obviously typing is not enforced in python
because it is dynamically typed. However, py developers often use type hints 
to add clarity to code. I thought I'd try it out because the compound types were 
getting a little confusing during this round of refactoring :)
'''

class SongOption(TypedDict):
    song: str
    artist: str

class PlaylistOption(TypedDict):
    playlist: List[SongOption]