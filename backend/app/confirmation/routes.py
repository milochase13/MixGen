from flask import request, session, redirect
from app.confirmation import bp
from app.commons.spotify_helpers import create_playlist
from app.commons.db import add_prompt, add_response, add_rating
import spotipy

@bp.route('/api/checklist', methods=['GET'])
def get_checklist():
    return {"checklist" : session["checklist"], "is_enough" : session["is_enough_responses"]}

@bp.route('/api/update-checklist', methods=['POST'])
def update_checklist():
    session["checklist"] = request.json['checklist']
    return {'success' : True}

@bp.route('/api/confirm-checklist', methods=['POST'])
def confirm_checklist():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/signin/')

    sp = spotipy.Spotify(auth_manager=auth_manager)

    uri_list = []
    prompt = session["prompt"]
    playlist_title = session["playlist_title"]
    song_uri = session["song_uri"]
    checklist = session["checklist"]
    for item in checklist.items():
        if item[1]:
            uri_list.append(song_uri[item[0]])
    create_playlist(sp, prompt, uri_list, playlist_title)

    ## Store in db
    msg_pmt, code_pmt  = add_prompt(prompt, playlist_title, session["num_songs"])

    if code_pmt == 201:
        session["pmt_id"] = msg_pmt["id"]
        for uri in uri_list:
            msg_res, code_res = add_response(uri, msg_pmt["id"])
            if code_res != 201:
                return {'error' : msg_res}
    else:
        return {'error' : msg_pmt}

    return {'success' : True}

@bp.route('/api/rating', methods=['POST'])
def record_rating():
    session["rating"] = request.json['rating']
    msg_pmt, code_pmt = add_rating(request.json['rating'], session["pmt_id"])
    return {'success' : True}
