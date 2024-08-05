from preprocess import Preprocessor, Normalizer, load_docs
from engine import create_positional_indexing, SearchEngine, query_scorer
import click





if __name__ == '__main__':
    docs = load_docs("./downloads/IR_data_news_12k.json", ["url", "content", "title"])
    normalizer = Normalizer("./downloads/verbs.dat")
    preprocessor = Preprocessor(normalizer, 20, "./downloads/verbs.dat")

    preprocessed_docs = preprocessor.preprocess(docs)

    search_engine = SearchEngine(create_positional_indexing, query_scorer, "./downloads", 50, preprocessor)
    search_engine.index_documents(preprocessed_docs)



