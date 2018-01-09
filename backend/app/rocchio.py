import numpy as np
from .tfidf import TFIDFQuery
from tools.ttdstokenizer import tokenize
from . import slides_index


# Relevance feedback weights, taken from
# https://nlp.stanford.edu/IR-book/pdf/09expand.pdf
QUERY_WEIGHT = 1
REL_DOC_WEIGHT = 0.75

FEEDBACK_TERM_NUM = 10


def rocchio(query_vec, rel_doc_vec):
    """Calculate Rocchio relevance feedback."""

    return QUERY_WEIGHT * query_vec + REL_DOC_WEIGHT * rel_doc_vec.sum(axis=0).A1 / rel_doc_vec.getnnz()


def feedback_terms(query, docs, smart):
    """Find n most relevance feedback terms given query and document UUIDs."""

    index = TFIDFQuery(slides_index)
    query_tokens = list(tokenize(query, True))
    query_nums = slides_index.toks_to_nums(query_tokens)

    # Fill numpy query vector from list of term scores
    query_vec = np.zeros((slides_index[:,:].shape[1]))
    for token, value in index.score_query(query_tokens, smart[3:])[1]:
        query_vec[slides_index.toks_to_nums(token)] = value

    # Get related document vectors from index
    rel_doc_vec = slides_index[docs,:]

    mod_query_vec = rocchio(query_vec, rel_doc_vec)

    # Set weights of existing terms to zero so that they would not be included in results
    mod_query_vec[query_nums] = 0

    result_nums = mod_query_vec.argsort()[:-FEEDBACK_TERM_NUM:-1]
    result_toks = slides_index.nums_to_toks(result_nums)

    return [dict(term=term, weight=weight) for term, weight in zip(result_toks, mod_query_vec[result_nums])]
