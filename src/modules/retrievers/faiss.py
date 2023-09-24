from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from pathlib import Path

class FaissRetriever:
    def __init__(self): 
        self.vectorstore=None

    def rebuild(self, collection_name: str, search_kwargs={ "k" : 5 },  newCollection_kwargs=None):
        if (collection_name is None or ''):
            raise ValueError(f'Error. Please provide a collection name.')
        vectorstore_file=Path(f'./{collection_name}.faiss')
        vectorstore_file.unlink(missing_ok=True)
        vectorstore_file=Path(f'./{collection_name}.pkl')
        vectorstore_file.unlink(missing_ok=True)
        self.build(collection_name, search_kwargs, newCollection_kwargs)
            
    def build(self, collection_name: str, search_kwargs={ "k" : 5 },  newCollection_kwargs=None):
        if (collection_name is None or ''):
            raise ValueError(f'Error. Please provide a collection name.')
        vectorstore_file=Path(f'./{collection_name}.faiss')
        if vectorstore_file.is_file():
             self.vectorstore = FAISS.load_local(folder_path='.', embeddings=OpenAIEmbeddings(),index_name=collection_name)
        else:
            # index not persisted
            if 'loader' not in newCollection_kwargs or \
                    'splitter' not in newCollection_kwargs or \
                    newCollection_kwargs['loader'] is None or \
                    newCollection_kwargs['splitter'] is None:
                    raise ValueError(f'Collection does not exist. Please provider a loader and a splitter to build the vector store.')

            docs = newCollection_kwargs['loader'].load()
            chunked_docs = newCollection_kwargs['splitter'].split_documents(docs)
            self.vectorstore = FAISS.from_documents(chunked_docs, embedding = OpenAIEmbeddings())
            self.vectorstore.save_local('.', index_name=collection_name)
        return self.getRetriever(**search_kwargs)
            
    def getRetriever(self, k=5, fetch_k=5, distance_metric='cos', maximal_marginal_relevance=True):
        
        # check Chroma collection has been created 
        if (self.vectorstore is None):
            raise ValueError(f'Error. Please setup a vector store first.')

        self.retriever = self.vectorstore.as_retriever()

        self.retriever.search_kwargs["distance_metric"] = distance_metric
        self.retriever.search_kwargs["fetch_k"] = fetch_k
        self.retriever.search_kwargs["maximal_marginal_relevance"] = maximal_marginal_relevance
        self.retriever.search_kwargs["k"] = k
        return self.retriever 