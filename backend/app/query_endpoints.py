from . import Handler, Schema, g, SMART_SCHEMA
from .rocchio import search_query, feedback_terms
from .inverted_index import slides_index, pages_index
from . import get_preview
from .tfidf import tfidf_test_instance

RESULTS_PER_PAGE = 18


@Handler('/search/pages', methods=['POST'], data_schema=Schema(cast=dict, schema={
    'query': Schema(cast=str, length=(3, 100)),
    'smart': SMART_SCHEMA,
    'page': Schema(cast=int, bounds=(0, 100))
}))
def search_pages_post():
    """
    Query search with optional relevance feedback.
    """
    scores = search_query(g.data['query'], g.data['smart'])
    sorted_scores = sorted(((score, uuid) for score, uuid in scores if score > 0), reverse=True)
    num_results = len(sorted_scores)

    results = [
        dict(
            uuid = uuid,
            tfidf = {'word1': 0.7071067811865475, 'word2': 0.5071067811865475},
            score = score,
            title = uuid,
            preview = get_preview(uuid, g.data['query']),
            url = pages_index.get_url(uuid)
        )
        for score, uuid in sorted_scores[g.data['page'] * RESULTS_PER_PAGE:(g.data['page'] + 1) * RESULTS_PER_PAGE]
    ]

    return {
        'pageCount': num_results // RESULTS_PER_PAGE + (num_results % RESULTS_PER_PAGE > 0),
        'queryWeights': {'queryWords1': 0.7071067811865475, 'word2': 0.5071067811865475},
        'results': results,
    }


@Handler('/search/slides', methods=['POST'], data_schema=Schema(cast=dict, schema={
    'query': Schema(cast=str, length=(3, 100)),
    'smart': SMART_SCHEMA,
    'page': Schema(cast=int, bounds=(0, 100))
}))
def search_slides_post():
    """
    Query search with optional relevance feedback.
    """
    scores = search_query(g.data['query'], g.data['smart'])
    sorted_scores = sorted(((score, uuid) for score, uuid in scores if score > 0), reverse=True)
    num_results = len(sorted_scores)
    results = [
       dict(
           uuid = uuid,
           score = score,
           title = uuid,
           content = 'Text here with highlights',
           url = slides_index.get_url(uuid)
       )
       for score, uuid in sorted_scores[g.data['page'] * RESULTS_PER_PAGE:(g.data['page'] + 1) * RESULTS_PER_PAGE]
    ]
    return {
        'pageCount': num_results // RESULTS_PER_PAGE + (num_results % RESULTS_PER_PAGE > 0),
        'results': results,
    }


@Handler('/search/feedback', methods=['POST'], data_schema=Schema(cast=dict, schema={
    'query': Schema(cast=str, length=(3, 100)),
    'docs': Schema(cast=list, length=(0, 100),
                   schema=Schema(cast=str, regex='[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}')),
    'smart': SMART_SCHEMA,
}))
def search_feedback_post():
    """
    Retrieve most relevant terms from documents.
    """
    term_weights = feedback_terms(g.data['query'], g.data['docs'], g.data['smart'])

    sorted_term_weights = sorted(term_weights.items(), key=lambda x: x[1], reverse=True)[:10]

    return [dict(term=term, weight=weight) for term, weight in sorted_term_weights]


@Handler('/tfidf_test', methods=['GET'], args_schema=Schema(cast=dict, schema={
    "q": Schema(cast=str, length=(3, 128)),
    "smart": SMART_SCHEMA
}))
def tfidf_test_get():
    # example query :
    # http://127.0.0.1:5000/tfidf_test?q=This%20is%20best&smart=lncLnc
    # crate test instance
    # i,test_documents = tfidf_test_instance(False)

    # example query with json inputs:
    # http://127.0.0.1:5000/tfidf_test?q=This%20document%20is%20a%20sample%20file&smart=ltcLnc

    # Create normal instance -> read from real the index
    i, test_documents = tfidf_test_instance(True)

    # Return dict as json
    return i.search(g.args['q'], g.args['smart'])
