from flask import request, session
from flask_cors import cross_origin
import json
from app.main import bp
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# helper functions
from app.commons.llm import query_openai
import app.commons.db
from app.commons.spotify_helpers import get_saved_songs
from app.commons.commons import sp

@bp.route('/api/submit', methods=['POST']) 
@cross_origin(headers=['Content-Type']) 
def submit():

    # Construct arguments
    response_body = request.json
    prompt = response_body['prompt']
    num_songs = response_body['num_songs']
    playlist_title = response_body['title']
    song_options, song_uri = get_saved_songs(sp) 
    song_options_stringified = " ,".join(song_options)

    # Make LLM API call
    gpt_response = query_openai(prompt, num_songs, song_options_stringified)
    # TESTING
    #gpt_response = "{\"playlist\": [\n {\"song\": \"Passionfruit\", \"artist\": \"Drake\"},\n {\"song\": \"Late in the Evening\", \"artist\": \"Paul Simon\"},\n {\"song\": \"What I Got\", \"artist\": \"Sublime\"}\n]}"
    
    # Construct response
    gpt_response_json = json.loads(gpt_response)
    song_list, uri_list = [], []
    song_uri_dict = {}
    for track in gpt_response_json["playlist"]:
        song_list.append("'"+track["song"]+"'"+ " by " + track["artist"])
        uri_list.append(song_uri[track["song"]+track["artist"]])
        song_uri_dict["'"+track["song"]+"'"+ " by " + track["artist"]] = song_uri[track["song"]+track["artist"]]
    song_list_stringified = "\n".join(song_list)
    

    # set session data
    session["checklist"] = dict.fromkeys(song_list, True)
    session["prompt"] = prompt
    session["playlist_title"] = playlist_title
    session["song_uri"] = song_uri_dict

    # Send server response
    api_response = {"playlist" : song_list_stringified}

    # TODO Store in DB

    return api_response