from . import Handler, Schema, g, SMART_SCHEMA
from .rocchio import feedback_terms
from .tfidf import search_query
from .inverted_index import slides_index, pages_index
from . import get_preview

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
    scores = search_query(pages_index, g.data['query'], g.data['smart'])
    sorted_scores = sorted(((score, uuid) for score, uuid in scores if score > 0), reverse=True)
    num_results = len(sorted_scores)

    results = [
        dict(
            uuid = uuid,
            tfidf = {'word1': 0.7071067811865475, 'word2': 0.5071067811865475},
            score = score,
            title = pages_index.get_title(uuid),
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
    scores = search_query(slides_index, g.data['query'], g.data['smart'])
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
    return feedback_terms(g.data['query'], g.data['docs'], g.data['smart'])
