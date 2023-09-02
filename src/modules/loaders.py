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
    