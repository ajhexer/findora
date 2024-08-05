import pickle
from pathlib import Path


class SearchEngine:
    def __init__(self, indexer, query_scorer, path_to_save,
                 champions_list_len, preprocessor,
                 indexed_documents=None,
                 documents_vectors=None):
        if documents_vectors is None:
            documents_vectors = {}
        if indexed_documents is None:
            indexed_documents = {}

        self.preprocessor = preprocessor
        self.indexer = indexer
        self.query_scorer = query_scorer
        self.path_to_save = path_to_save
        self.champions_list_len = champions_list_len
        self.indexed_documents = indexed_documents
        self.documents_vectors = documents_vectors
        self.raw_docs = None

    def index_documents(self, documents):
        indexed_documents, document_vectors = self.indexer(documents, self.champions_list_len)
        self.indexed_documents = indexed_documents
        self.documents_vectors = document_vectors
        self.raw_docs = documents

    def search(self, query, result_window, similarity_type, tf=False, print_results=False, champions_list=False):
        tokens = self.preprocessor.query_preprocess(query)
        result = self.query_scorer(tokens, self.indexed_documents, self.documents_vectors,
                                   result_window, self.raw_docs, similarity_type, tf,  champions_list)
        if print_results:
            self.__print_results(result)
        return result

    def save(self):
        pickle.dump(self.indexed_documents, open(Path(self.path_to_save, "indexes"), 'wb'))
        pickle.dump(self.documents_vectors, open(Path(self.path_to_save, "vectors"), 'wb'))

    def load(self):
        self.indexed_documents = pickle.load(open(Path(self.path_to_save, "indexes"), 'rb'))
        self.documents_vectors = pickle.load(open(Path(self.path_to_save, "vectors"), 'rb'))


    def __print_results(self, results):
        for rank, result in enumerate(results):
            doc_id = result[0]
            if doc_id is None:
                continue
            print(100 * '-' + '\n')
            print(f"""
            Rank: {rank + 1}
            Document ID: {doc_id}
            Title: {self.raw_docs[doc_id]['title']}
            Url: {self.raw_docs[doc_id]['url']}
            Score: {result[1]}
            """)




