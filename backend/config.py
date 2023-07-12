import os

class Config:
    SECRET_KEY = os.environ['SESSION_SECRET']