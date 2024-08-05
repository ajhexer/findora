from collections import Counter
from .utils import calculate_tf, vector_length


def query_scorer(query_tokens, dictionary, docs_vectors,
                 result_window, raw_docs, similarity_type="cosine", tf=False, champions_list=False):
    if similarity_type == "cosine":
        return query_scorer_cosine(query_tokens, dictionary, docs_vectors, result_window, tf, champions_list)
    elif similarity_type == "jaccard":
        return query_scorer_jaccard(query_tokens, dictionary, raw_docs, result_window, champions_list)


def query_scorer_cosine(query_tokens, dictionary, docs_vectors, result_window, tf=False, champions_list=False):
    tokens_count = dict(Counter(query_tokens))
    cosine_scores = {}
    for term, term_count in tokens_count.items():
        if term in dictionary:
            if champions_list:
                term_docs = dictionary[term]['champions_list']
            else:
                term_docs = dictionary[term]['docs']

            w_tq = calculate_tf(term_count)

            for doc_id, doc in term_docs.items():
                w_td = docs_vectors[doc_id][term]['tf'] if tf else doc['tf_idf']
                # # w_td = doc['tf_idf']
                # w_td = docs_vectors[doc_id]['tf']
                if doc_id in cosine_scores:
                    cosine_scores[doc_id] += w_td * w_tq
                else:
                    cosine_scores[doc_id] = w_td * w_tq

    for doc_number in cosine_scores:
        cosine_scores[doc_number] /= vector_length(docs_vectors[str(doc_number)])

    sorted_cosine = sorted(cosine_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_cosine[:min(result_window, len(sorted_cosine))]


def query_scorer_jaccard(query_tokens, dictionary, raw_docs, result_window, champions_list=False):
    jaccard_scores = {}
    tokens_count = dict(Counter(query_tokens))
    for term, term_count in tokens_count.items():
        if term in dictionary:
            if champions_list:
                term_docs = dictionary[term]['champions_list']
            else:
                term_docs = dictionary[term]['docs']

            for doc_id in term_docs:
                if doc_id in jaccard_scores:
                    jaccard_scores[doc_id] += 1
                else:
                    jaccard_scores[doc_id] = 1

    for doc_number in jaccard_scores:
        jaccard_scores[doc_number] /= (
                    len(set(raw_docs[doc_number]['content']).union(set(tokens_count.keys()))))

    sorted_doc_jaccard = sorted(jaccard_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_doc_jaccard[:min(result_window, len(sorted_doc_jaccard))]