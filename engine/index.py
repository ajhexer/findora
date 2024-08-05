import numpy as np
import tqdm


def create_positional_indexing(docs, champions_list_len):
    docs_index = {}
    for doc_id, doc in tqdm.tqdm(docs.items()):
        for position, token in enumerate(doc["content"]):
            if token in docs_index:
                if doc_id in docs_index[token]['docs']:
                    docs_index[token]['docs'][doc_id]['positions'].append(position)
                    docs_index[token]['docs'][doc_id]['per_doc_frequency'] += 1
                else:
                    docs_index[token]['docs'][doc_id] = {
                        'positions': [position],
                        'per_doc_frequency': 1,
                    }
                docs_index[token]['frequency'] += 1
            else:
                docs_index[token] = {
                    'frequency': 1,
                    'docs': {
                        doc_id:
                            {
                                'positions': [position],
                                'per_doc_frequency': 1,
                            }
                    }
                }

    total_docs = len(docs)
    docs_vector = {}
    for term in tqdm.tqdm(docs_index):
        term_docs = dict(docs_index[term]['docs'])
        n_t = len(term_docs.keys())
        for doc_id, doc in term_docs.items():
            tf = doc['per_doc_frequency']
            tf_idf = (np.log10(total_docs/n_t))*(1+np.log10(tf))
            docs_index[term]['docs'][doc_id]['tf_idf'] = tf_idf
            if doc_id not in docs_vector:
                docs_vector[doc_id] = {}
            docs_vector[doc_id][term] = {'tf_idf': tf_idf, 'tf': tf}

        sorted_term_doc = sorted(term_docs, key=lambda x: term_docs[x]['per_doc_frequency'], reverse=True)
        docs_index[term]['champions_list'] = {doc_id: {'per_doc_frequency':
                                                        docs_index[term]['docs'][doc_id]['per_doc_frequency'],
                                                       'tf_idf': docs_index[term]['docs'][doc_id]['tf_idf'],}
                                                        for doc_id in sorted_term_doc}
        if champions_list_len < n_t:
            docs_index[term]['champions_list'] = dict(list(docs_index[term]['champions_list'].items())
                                                      [:champions_list_len])

    return docs_index, docs_vector
