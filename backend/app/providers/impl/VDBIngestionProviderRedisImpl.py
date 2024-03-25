from langchain_community.vectorstores import Redis
from app.providers.VDBIngestionProviderBase import VDBIngestionProvider

class VDBIngestionProviderRedisImpl(VDBIngestionProvider):

    def __init__(self, embedder, index_name, index_schema, redis_url):
        self.embedder = embedder
        self.index_name = index_name
        self.index_schema = index_schema
        self.redis_url = redis_url

    def ingest_lyrics(self, chunks: str, metadatas):
        """
        Ingest the lyrics of the user's saved songs
        """

        print("Parsing songs")

        # Create vectorstore
        songs = []
        for i, chunk in enumerate(chunks):
            songs.append(metadatas[i]["titles"] + chunk)

        _ = Redis.from_texts(
            texts=songs,
            metadatas=metadatas,
            embedding=self.embedder,
            index_name=self.index_name,
            index_schema=self.index_schema,
            redis_url=self.redis_url,
        )