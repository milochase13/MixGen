import spotipy
from flask import session, request
from app.main import bp

scope = ["user-library-read","playlist-modify-private"]

@bp.route('/signin/geturl')
def get_url():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    auth_url = auth_manager.get_authorize_url()
    return {'auth_url' : auth_url}

@bp.route('/signin/')
def index():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=scope,
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    if request.args.get("code"):
        auth_manager.get_access_token(auth_manager.parse_response_code(request.url))
        return {'success': True}
    