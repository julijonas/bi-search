import numpy as np
from .tfidf import ProximityIndex
from tools.ttdstokenizer import tokenize
from . import slides_index

original_weight = 0.4
related_weight = 0.3


def multiply(vector, scalar):
    return {no: v * scalar for no, v in vector.items()}


def add(vector1, vector2):
    result = vector1.copy()
    for no, v in vector2.items():
        result[no] = result.get(no, 0) + v
    return result


def add_all(vectors):
    result = vectors[0].copy()
    for vector in vectors[1:]:
        for no, v in vector.items():
            result[no] = result.get(no, 0) + v
    return result


def rocchio(original_query, related_docs):
    return add(multiply(original_query, original_weight),
               multiply(add_all(related_docs), related_weight / len(related_docs)))


def search_query(query, smart):
    index = ProximityIndex(None)
    rankings, sorted_scores = index.ranked_search_cos(query, smart)
    return rankings


def feedback_terms(query, docs, smart):
    index = ProximityIndex(None)

    query_tokens = list(tokenize(query, True))
    original_query = dict(index.score_query(query_tokens, smart[3:])[1])

    docs = list(docs)
    small_index = slides_index[docs, :]
    occurrences = small_index.sum(axis=0)
    print(occurrences.shape)
    occurring = np.argsort(occurrences)[0,-10:].A1

    occurring = slides_index.nums_to_toks(occurring)

    related_documents = [dict(index.score_documents(occurring, doc, smart[:3])[1]) for doc in docs]
    modified_query = rocchio(original_query, related_documents)

    for token in query_tokens:
        if token in modified_query:
            del modified_query[token]

    return modified_query


if __name__ == '__main__':
    print(search_query('content', ['06c0707a-7af7-4fe4-9417-ca1474b01370']))
