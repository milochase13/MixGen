import os

user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
db_name = 'mix_gen'

class Config:
    SECRET_KEY = os.environ['SESSION_SECRET']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@localhost:5432/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_ORIGIN = "http://locadafadlhost:5000/"  #os.environ['CORS_ALLOW_ORIGIN']