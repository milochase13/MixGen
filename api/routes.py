# from flask import current_app,jsonify,request
# import requests
# import psycopg2
# from api import app
# import time
# from flask_cors import CORS 
# import sys
# import logging


# # conn = psycopg2.connect(
# #     host="localhost",
# #     database="your_database",
# #     user="your_username",
# #     password="your_password"
# # )

# CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'


# @app.route('/api/time')
# def get_current_time():
#     return {'time': time.time()}

# @app.route('/api/submit', methods=['POST']) 
# @cross_origin(headers=['Content-Type']) 
# def submit():
#     response_body = request.json.get('response', '')
#     print(response_body)

#     # Make API call
#     api_response = {"test":"test"}#requests.get('https://api.example.com', params={'query': response_body})
#     api_data = api_response.json()

#     # Store result in PostgreSQL
#     # cursor = conn.cursor()
#     # cursor.execute("INSERT INTO results (response) VALUES (%s)", (response_body,))
#     # conn.commit()
#     # cursor.close()

#     return jsonify(api_data)

