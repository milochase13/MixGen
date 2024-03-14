import os

user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
db_name = 'mix_gen'

EMBED_MODEL=os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
REDIS_URL=os.environ["REDIS_URL"]
INDEX_NAME=os.getenv("INDEX_NAME", "rag-redis")
INDEX_SCHEMA="/Users/milochase/projects/MixGen/backend/app/configs/redisRagLyricsSchema.yaml"
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

class Config:
    SECRET_KEY = os.environ['SESSION_SECRET']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@localhost:5432/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_ORIGIN = "http://locadafadlhost:5000/"  #os.environ['CORS_ALLOW_ORIGIN']