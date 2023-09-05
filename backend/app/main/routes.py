from flask import request, session, redirect
from flask_cors import cross_origin
from app.main import bp
import os
import sys
import spotipy

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# helper functions
from app.commons.llm import query_openai
import app.commons.db
from app.commons.spotify_helpers import get_saved_songs

@bp.route('/api/submit', methods=['POST']) 
@cross_origin(headers=['Content-Type']) 
def submit():
    # Create Spotify object from cache, fallback redirect to signin
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/signin/')
    
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Construct arguments
    response_body = request.json
    prompt = response_body['prompt']
    num_songs = response_body['num_songs']
    playlist_title = response_body['title']
    song_options, song_uri = get_saved_songs(sp) 

    # Make LLM API call
    gpt_response = query_openai(prompt, int(num_songs), song_options)
    # TESTING
    # gpt_response = "{\"playlist\": [\n {\"song\": \"Passionfruit\", \"artist\": \"Drake\"},\n {\"song\": \"Late in the Evening\", \"artist\": \"Paul Simon\"},\n {\"song\": \"What I Got\", \"artist\": \"Sublime\"}\n]}"

    # Construct response
    song_list, uri_list = [], []
    song_uri_dict = {}
    for track in gpt_response:
        try:
            uri_list.append(song_uri[track[0]+track[1]])
        except:
            # TODO bad key callback
            print("BAD KEY: "+track[0]+track[1])
            continue
        else:
            song_list.append("'"+track[0]+"'"+ " by " + track[1])
            song_uri_dict["'"+track[0]+"'"+ " by " + track[1]] = song_uri[track[0]+track[1]]
    song_list_stringified = "\n".join(song_list)

    # Set session data
    session["checklist"] = dict.fromkeys(song_list, True)
    session["prompt"] = prompt
    session["playlist_title"] = playlist_title
    session["song_uri"] = song_uri_dict
    session["num_songs"] = num_songs

    # Send server response
    api_response = {"playlist" : song_list_stringified}

    return api_response
