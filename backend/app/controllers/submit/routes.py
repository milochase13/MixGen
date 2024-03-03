from flask import request, session, redirect
from flask_cors import cross_origin
from app.controllers.submit import bp
import os
import sys
import spotipy
from app.providers.impl.getSongOptionsGPTImpl import GetSongOptionsProviderGPTImpl

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

# helper functions
from app.commons.spotify_helpers import get_saved_songs

@bp.route('/api/submit', methods=['POST']) 
@cross_origin(headers=['Content-Type']) 
def submit():
    # Create Spotify object from cache, fallback redirect to signin
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    system_prompt="""You are a helpful assistant. Your job is to recommend songs
      for a music playlist given a list of song options. If you don't know a 
      song, you can make a guess based on the title and artist, but be more 
      cautious. You will give your response in a JSON format with the following 
      schema: {"playlist": [{"song": String, "artist": String}]}. Do not include
        any text in your response other than the JSON output."""
    user_prompt_template="""I want to create a playlist that is: {}. Given the 
      following song options (in no particular order, try to consider each song 
      equally), create an appropriate playlist that is {} songs with your very 
      best picks towards the beginning. Song options: """
    get_song_options_provider = GetSongOptionsProviderGPTImpl(
        model="gpt-3.5-turbo", system_prompt=system_prompt, 
        user_prompt_template=user_prompt_template, 
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        batch_size=1000)

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
    llm_response, backup = get_song_options_provider.get_songs(prompt, int(num_songs), song_options)
    # TESTING
    # llm_response = [{'song': 'The Modern Age', 'artist': 'The Strokes'}, {'song': 'We Will Rock You', 'artist': 'Queen'}, {'song': "Don't Stop Me Now", 'artist': 'Queen'}]
    #backup = [{'song': 'Another One Bites the Dust', 'artist': 'Queen'}, {'song': 'Somebody to Love', 'artist': 'Queen'}, {'song': 'Under Pressure', 'artist': 'Queen'}]

    # Construct response
    song_list, uri_list, song_uri_dict, is_enough_responses = [], [], {}, True
    while llm_response:
        track = llm_response[0]
        try:
            uri_list.append(song_uri[track["song"]+track["artist"]])
            llm_response.pop(0)
        except:
            llm_response.pop(0)
            if len(backup) > 0:
                llm_response.append(backup.pop())
            else:
                is_enough_responses = False
        else:
            song_list.append("'"+track["song"]+"'"+ " by " + track["artist"])
            song_uri_dict["'"+track["song"]+"'"+ " by " + track["artist"]] = song_uri[track["song"]+track["artist"]]
    song_list_stringified = "\n".join(song_list)

    # Set session data
    session["checklist"] = dict.fromkeys(song_list, True)
    session["prompt"] = prompt
    session["playlist_title"] = playlist_title
    session["song_uri"] = song_uri_dict
    session["num_songs"] = num_songs
    session['is_enough_responses'] = is_enough_responses

    # Send server response
    api_response = {"playlist" : song_list_stringified, "is_enough_responses": is_enough_responses}

    return api_response