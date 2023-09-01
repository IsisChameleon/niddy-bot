import os
from langchain.document_loaders import CSVLoader
from langchain.document_loaders.pdf import PDFPlumberLoader

class MyDirectoryLoader:

    def __init__(self, dir_path):
        self.dir_path = dir_path
        
    def check_args(self):
        print(**self.pdf_args.keys())

    def load(self):
        docs = []
        for root, _, files in os.walk(self.dir_path):
            for file in files:
                print('file:', file)
                file_path = os.path.join(root, file)
                if file_path.endswith('.csv'):
                    loader = CSVLoader(file_path)
                elif file_path.endswith('.pdf'):
                    loader = PDFPlumberLoader(file_path)
                else:
                    print(f"Do not process the file: {file_path}")
                    continue
                loaded_docs = loader.load()
                docs.extend(loaded_docs)
        return docs
    
# class Chunker:
#     def __init__(self, loader, splitter):
#         self.loader = loader
#         self.splitter = splitter
        
#     def chunk(self):
#         docs = self.loader.load()
#         chunked_docs = self.splitter.split_documents(docs)
#         return chunked_docs
    
# splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
# chunked_docs = splitter.split_documents(docs)