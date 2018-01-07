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


def feedback_terms(query, docs, smart):
    # index = ProximityIndex(slides_index)
    #
    # query_tokens = list(tokenize(query, True))
    # original_query = dict(index.score_query(query_tokens, smart[3:])[1])
    #
    # docs = list(docs)
    # small_index = slides_index[docs, :]
    # occurrences = small_index.sum(axis=0)
    # print(occurrences.shape)
    # occurring = np.argsort(occurrences)[0,-10:].A1
    #
    # occurring = slides_index.nums_to_toks(occurring)
    #
    # related_documents = [dict(index.score_documents(occurring, doc, smart[:3])[1]) for doc in docs]
    # # related_documents = docs
    # modified_query = rocchio(original_query, related_documents)
    #
    # for token in query_tokens:
    #     if token in modified_query:
    #         del modified_query[token]

    return {
        "informatics": 2.1,
        "slides": 1.9
    }
    return modified_query
