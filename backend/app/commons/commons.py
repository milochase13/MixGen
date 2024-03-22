from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Redis
from config import EMBED_MODEL, INDEX_NAME, INDEX_SCHEMA, REDIS_URL

"""
https://js.langchain.com/docs/integrations/document_loaders/file_loaders/directory
https://python.langchain.com/docs/modules/data_connection/document_loaders/file_directory
https://js.langchain.com/docs/integrations/document_loaders/file_loaders/directory
https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.unstructured.UnstructuredFileLoader.html
"""

def ingest_documents():
    """
    Ingest Lyrics files to Redis from the songLyrics/ directory
    """
    data_path = "songLyrics/"

    loader = DirectoryLoader(data_path)
    lyricFiles = loader.load() 

    print("Done preprocessing. Created", len(lyricFiles), "lyricFiles") 
    # Create vectorstore
    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    _ = Redis.from_texts(
        # appending this little bit can sometimes help with semantic retrieval
        # especially with multiple companies
        texts=[lyricFile.page_content for lyricFile in lyricFiles],
        metadatas=[lyricFile.metadata for lyricFile in lyricFiles],
        embedding=embedder,
        index_name=INDEX_NAME,
        index_schema=INDEX_SCHEMA,
        redis_url=REDIS_URL,
    )
