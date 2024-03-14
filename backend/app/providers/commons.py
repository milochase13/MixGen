from typing import List
from app.providers.types import PlaylistOption, SongOption
import json

''' 
parse_response_options(get_song_options_batches: PlaylistOption): [SongOption]
helper function that takes all batches of song options returned from model
and returns a single list of all batches combined 

TODO: better error handling. Currently, if a batch is not in JSON format,
it will just skip it. 
'''

def combine_response_options(get_song_options_batches: PlaylistOption) ->  List[SongOption]:
    response_batches_combined = []
    for get_song_options in get_song_options_batches:
        try:
            response_options_json = json.loads(get_song_options)
            response_batches_combined.extend(response_options_json["playlist"])
        except:
            # Will propogate empty result through workflow until eventually being handled later if there is not enough data
            continue
    return response_batches_combined