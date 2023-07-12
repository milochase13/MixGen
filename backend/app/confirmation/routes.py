from flask import request, session
from app.confirmation import bp
from app.commons.spotify_helpers import create_playlist
from app.commons.commons import sp

@bp.route('/api/checklist', methods=['GET'])
def get_checklist():
    if session["checklist"]:
        return session["checklist"]

@bp.route('/api/update-checklist', methods=['POST'])
def update_checklist():
    session["checklist"] = request.json['checklist']
    return {'success' : True}

@bp.route('/api/confirm-checklist', methods=['POST'])
def confirm_checklist():
    uri_list = []
    prompt = session["prompt"]
    playlist_title = session["playlist_title"]
    song_uri = session["song_uri"]
    checklist = session["checklist"]
    for item in checklist.items():
        if item[1]:
            uri_list.append(song_uri[item[0]])
    create_playlist(sp, prompt, uri_list, playlist_title)
    return {'success' : True}