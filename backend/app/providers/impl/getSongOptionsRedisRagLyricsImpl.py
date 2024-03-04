'''
Load lyrics data for each saved song (preloading, should be done async at signin)
'''

'''
Ingest the data into running Redis instance (preloading, should be done async at signin)
'''

'''
Connect to pre-loaded vectorstore and instantiate a retriever with it
'''

'''
Create RAG chain with LangChain
'''

'''
Implement get_songs api using the RAG chain
'''

'''
References:
1. https://redis.com/blog/announcing-langchain-rag-template-powered-by-redis/
2. https://medium.com/@kv742000/creating-a-python-server-for-document-q-a-using-langchain-31a123b67935
'''

from app.providers.getSongOptionsBase import GetSongOptionsProvider
from app.providers.types import RagQuestion
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Redis
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

class GetSongOptionsProviderRedisRagLyricsImpl(GetSongOptionsProvider):

    def __init__(self, user_prompt, embedder, index_name, index_schema, redis_url, template):
        self.user_prompt = user_prompt
        self.embedder = embedder
        self.index_name = index_name
        self.index_schema = index_schema
        self.redis_url = redis_url
        self.template = template
        
    def connect_to_vector_store(self):
        vectorstore = Redis.from_existing_index(
            embedding=self.embedder, index_name=self.index_name, schema=self.index_schema, redis_url=self.redis_url
        )
        retriever = vectorstore.as_retriever(search_type="mmr")
        return retriever
    
    def create_rag_chain(self, retriever):
        prompt = ChatPromptTemplate.from_template(self.template)

        # RAG Chain
        model = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
        chain = (
            RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            | prompt
            | model
            | StrOutputParser()
        ).with_types(input_type=RagQuestion)
        return chain
    
    def get_songs(self):
        vector_store = self.connect_to_vector_store()
        rag_chain = self.create_rag_chain(vector_store)
        response = rag_chain(self.user_prompt) # I think that's how this works?
        return response, []
