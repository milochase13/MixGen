def get_saved_songs(sp):
    song_options = []
    song_uri = {}
    results = sp.current_user_saved_tracks()
    for _, item in enumerate(results['items']):
        track = item['track']
        song_options.append("'" + track['name'] + "'" + " by " + track['artists'][0]['name'])
        song_uri[track['name']+track['artists'][0]['name']] = track['uri']
    return song_options, song_uri


def create_playlist(sp, prompt, uris, title):
    user_id = sp.current_user()['id']
    if title == '':
        title = 'AI generated playlist'
    playlist_response = sp.user_playlist_create(user=user_id, name=title, public=False, description=prompt)
    playlist_id = playlist_response['id']
    sp.playlist_add_items(playlist_id, uris)