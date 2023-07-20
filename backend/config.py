import os

user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']

class Config:
    SECRET_KEY = os.environ['SESSION_SECRET']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@localhost:5432/mix_gen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False