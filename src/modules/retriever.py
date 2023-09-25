from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from chromadb.config import Settings
# from chromadb import HttpClient
from chromadb import Client
from chromadb.api import API

class ChromaRetriever:
    
    _localhost_client_settings = Settings(
            chroma_api_impl="rest",
            chroma_server_host="host.docker.internal",  # when you run this inside a devcontainer you need to explicitely say host.docker.internal to signify "devcontainer host localhost"
            chroma_server_http_port="8000")
    _persistent_client_settings = Settings(
            chroma_db_impl="duckdb+parquet")
    
    def __init__(self, client_type='ephemeral', client_settings=None):    
        
        self.client_settings = None
        if client_type not in ['ephemeral', 'persistent', 'httpclient']:
            raise ValueError(f"Please input existing client type: 'ephemeral', 'persistent', 'httpclient'")
        
        if client_type == 'ephemeral':
            self.client: API = Client()
        else:
            if client_type == 'persistent':
                self.client_settings = client_settings or self._persistent_client_settings
            if client_type == 'httpclient':
                self.client_settings = client_settings or self._localhost_client_settings
            self.client: API = Client(settings=self.client_settings)
            
        self.chromaDb = None
    
    def rebuild(self, collection_name: str, search_kwargs={ "k" : 5 },  newCollection_kwargs=None):
        if (collection_name is None or ''):
            raise ValueError(f'Error. Please provide a collection name.')

        collections = self.client.list_collections()
        names = [c.name for c in collections]
        if collection_name in names:
            self.client.delete_collection(name=collection_name)

        return self.build(collection_name, search_kwargs, newCollection_kwargs)
    
    def build(self, collection_name: str, search_kwargs={ "k" : 5 },  newCollection_kwargs=None):
        if (collection_name is None or ''):
            raise ValueError(f'Error. Please provide a collection name.')

        try:
            self.client.get_collection(name=collection_name, embedding_function=OpenAIEmbeddings())
        except Exception :
            if 'loader' not in newCollection_kwargs or \
                'splitter' not in newCollection_kwargs or \
                newCollection_kwargs['loader'] is None or \
                newCollection_kwargs['splitter'] is None:
                raise ValueError(f'Collection does not exist. Please provider a loader and a splitter to build the vector store.')

            docs = newCollection_kwargs['loader'].load()
            chunked_docs = newCollection_kwargs['splitter'].split_documents(docs)
            
            self.chromaDb = Chroma.from_documents(chunked_docs, client_settings=self.client_settings, embedding = OpenAIEmbeddings(), collection_name=collection_name)
        else:
            self.chromaDb = Chroma(collection_name, embedding_function=OpenAIEmbeddings(), client_settings=self.client_settings)
        finally:
            return self.getRetriever(**search_kwargs)
        
    def getRetriever(self, k=5, fetch_k=5, distance_metric='cos', maximal_marginal_relevance=True):
        
        # check Chroma collection has been created 
        if (self.chromaDb is None):
            raise ValueError(f'Error. Please setup a vector store in Chroma first.')

        self.retriever = self.chromaDb.as_retriever()

        self.retriever.search_kwargs["distance_metric"] = distance_metric
        self.retriever.search_kwargs["fetch_k"] = fetch_k
        self.retriever.search_kwargs["maximal_marginal_relevance"] = maximal_marginal_relevance
        self.retriever.search_kwargs["k"] = k
        return self.retriever
        
        '''
        Note about maximal relevance search:
        
        .../site-packages/langchain/vectorstores/base.py
        
        Maximal marginal relevance optimizes for similarity to query AND diversity
        among selected documents.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            fetch_k: Number of Documents to fetch to pass to MMR algorithm.
            lambda_mult: Number between 0 and 1 that determines the degree
                        of diversity among the results with 0 corresponding
                        to maximum diversity and 1 to minimum diversity.
                        Defaults to 0.5.
        Returns:
            List of Documents selected by maximal marginal relevance.
        ''' 