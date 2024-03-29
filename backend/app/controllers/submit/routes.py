from flask import request, session, redirect
from flask_cors import cross_origin
from app.controllers.submit import bp
import os
import sys
import spotipy
from app.providers.impl.getSongOptionsGPTImpl import GetSongOptionsProviderGPTImpl
from app.providers.impl.getSongOptionsRedisRagLyricsImpl import GetSongOptionsProviderRedisRagLyricsImpl
from app.providers.impl.SongDetailsProviderGeniusImpl import SongDetailsProviderGeniusImpl
from app.providers.impl.VDBIngestionProviderRedisImpl import VDBIngestionProviderRedisImpl
from app.configs import getSongOptionsProviderGPTConfig as GPTConfig, getSongOptionsRedisRagLyricsConfig as RRLConfig
from langchain_community.embeddings import HuggingFaceEmbeddings
import config as AppConfig

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from app.commons.spotify_helpers import get_saved_songs

@bp.route('/api/submit', methods=['POST']) 
@cross_origin(headers=['Content-Type']) 
def submit():
    # Create Spotify object from cache, fallback redirect to signin
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    # Instantiate clients
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/signin/')
    
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Construct arguments
    response_body = request.json
    prompt = response_body['prompt']
    num_songs = response_body['num_songs']
    playlist_title = response_body['title']
    song_options, song_uri = get_saved_songs(sp)

    # Instantiate providers
    get_song_options_batched_gpt_provider = GetSongOptionsProviderGPTImpl(
        song_choices=song_options,
        model=GPTConfig.MODEL, system_prompt=GPTConfig.SYSTEM_PROMPT, 
        user_prompt_template=GPTConfig.USER_PROMPT_TEMPLATE, 
        openai_api_key=AppConfig.OPENAI_API_KEY,
        batch_size=GPTConfig.BATCH_SIZE,
        max_batching_depth=GPTConfig.MAX_BATCHING_DEPTH,
        )
    
    get_song_options_rrl_provider = GetSongOptionsProviderRedisRagLyricsImpl(
        embedder=HuggingFaceEmbeddings(model_name=AppConfig.EMBED_MODEL),
        index_name=AppConfig.INDEX_NAME,
        index_schema=AppConfig.INDEX_SCHEMA,
        redis_url=AppConfig.REDIS_URL,
        context_template=RRLConfig.CONTEXT_TEMPLATE,
        response_schema=RRLConfig.RESPONSE_SCHEMA,
    )

    geniusSongDetails = SongDetailsProviderGeniusImpl('TODO add')
    testSongOptions = [{"song": "Happy", "artist": "Pharrell Williams"}, {"song": "Friend is a four letter word", "artist": "Cake"}, {"song": "PRIDE", "artist": "Kendrick Lamar"}]
    lyrics = geniusSongDetails.get_all_lyrics(testSongOptions)
    print(lyrics)

    vdbIngestion = VDBIngestionProviderRedisImpl(
        embedder=HuggingFaceEmbeddings(model_name=AppConfig.EMBED_MODEL),
        index_name=AppConfig.INDEX_NAME,
        index_schema=AppConfig.INDEX_SCHEMA,
        redis_url=AppConfig.REDIS_URL,
        )
    
    # lyrics = {
    #     'Happy by Pharrell Williams': 'happy',
    #     'Friend is a four letter word by Cake': 'sad',
    #     'PRIDE by Kendrick Lamar': 'emotional',
    # }

    vdbIngestion.ingest_lyrics(list(lyrics.values()), [{'titles': key} for key in list(lyrics.keys())])
    

    # Make LLM API call
    llm_response, backup = get_song_options_rrl_provider.get_songs(prompt, int(num_songs))

    print("response: ", llm_response)

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