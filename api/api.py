from flask import Flask, request
from flask_cors import CORS, cross_origin
import time
import openai
import psycopg2
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

app = Flask(__name__)
CORS(app)

scope = ["user-library-read","playlist-modify-private"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def create_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="your_username",
        password="your_password",
        database="your_database_name"
    )
    return conn

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

def query_openai(prompt, num_songs, song_options):
    #system_prompt = "You are a helpful assistant. Your job is to recommend songs for a music playlist given a list of song options. If you don't know a song, make an educated guess based on its name and artist, but be more conservative when choosing to recommend it. You will give your response in a JSON format with the following schema: {\"playlist\": [{\"song\": String, \"artist\": String}]}. Do not include any text in your response other than the JSON output."
    system_prompt = "You are a helpful assistant. Your job is to recommend songs for a music playlist given a list of song options. You will give your response in a JSON format with the following schema: {\"playlist\": [{\"song\": String, \"artist\": String}]}. Do not include any text in your response other than the JSON output."
    user_prompt = "I want to create a playlist that is: " + prompt + ". Given the following song options, create an appropriate playlist that is " + str(num_songs) + " songs long. Song options: " + song_options
    openai.api_key = os.getenv("OPENAI_API_KEY")
    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
    )
    response_message = gpt_response["choices"][0]['message']['content']
    return response_message


@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/api/submit', methods=['POST']) 
@cross_origin(headers=['Content-Type']) 
def submit():

    # Construct arguments
    response_body = request.json
    prompt = response_body['prompt']
    num_songs = response_body['num_songs']
    playlist_title = response_body['title']
    song_options, song_uri = get_saved_songs(sp) #["'Happy' by Pharrell Williams", "'Walking on Sunshine' by Katrina & The Waves", "'The Boxer' by Simon and Garfunkel", "'Good Vibrations' by the Beach Boys", "'Trouble' by Cat Stevens"]
    song_options_stringified = " ,".join(song_options)

    # Make API call
    #gpt_response = query_openai(prompt, num_songs, song_options_stringified)
    # TESTING
    gpt_response = "{\"playlist\": [\n {\"song\": \"Passionfruit\", \"artist\": \"Drake\"},\n {\"song\": \"Late in the Evening\", \"artist\": \"Paul Simon\"},\n {\"song\": \"What I Got\", \"artist\": \"Sublime\"}\n]}"
    
    # Construct response
    gpt_response_json = json.loads(gpt_response)
    song_list, uri_list = [], []
    for track in gpt_response_json["playlist"]:
        song_list.append("'"+track["song"]+"'"+ " by " + track["artist"])
        uri_list.append(song_uri[track["song"]+track["artist"]])
    song_list_stringified = "\n".join(song_list)

    # TODO add user-confirmation

    # Create playlist
    create_playlist(sp, prompt, uri_list, playlist_title)

    # Send server response
    api_response = {"playlist" : song_list_stringified}

    # TODO Store in DB

    #conn = create_db_connection()

    # Store result in PostgreSQL
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO results (response) VALUES (%s)", (response))
    # conn.commit()
    # cursor.close()

    return api_response

if __name__ == '__main__':
    app.run()