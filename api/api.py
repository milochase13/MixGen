from flask import Flask
from flask_cors import CORS, cross_origin
import time
from flask import request
import psycopg2

app = Flask(__name__)
CORS(app)

def create_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="your_username",
        password="your_password",
        database="your_database_name"
    )
    return conn


@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/submit', methods=['POST']) 
@cross_origin(headers=['Content-Type']) 
def submit():
    response_body = request.json
    response = response_body['response']
    
    # Make API call
    
    

    api_response = {"prompt" : response}

    #conn = create_db_connection()

    # Store result in PostgreSQL
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO results (response) VALUES (%s)", (response))
    # conn.commit()
    # cursor.close()

    return api_response

if __name__ == '__main__':
    app.run()