from . import Handler, Schema, g, SMART_SCHEMA
from .rocchio import search_query, feedback_terms
from .indexing import slides_index


RESULTS_PER_PAGE = 18


@Handler('/q/search', methods=['POST'], data_schema=Schema(cast=dict, schema={
    'mode': Schema(cast=str, values=('slides', 'pages')),
    'query': Schema(cast=str, length=(3, 100)),
    'smart': SMART_SCHEMA,
    'page': Schema(cast=int, bounds=(0, 100))
}))
def search_get():
    """
    Query search with optional relevance feedback.
    """
    mode = g.data['mode']
    page = g.data['page']
    scores = search_query(g.data['query'], g.data['smart'])
    sorted_scores = sorted(((score, uuid) for score, uuid in scores if score > 0), reverse=True)
    num_results = len(sorted_scores)
    if mode == 'pages':
       results = [
           dict(
               uuid = uuid,
               tfidf = {'word1': 1.2, 'word2': 3.2},
               score = score,
               title = uuid,
               content = 'Text here with highlights',
               url = 'http://example.com'
           )
           for score, uuid in sorted_scores[page * RESULTS_PER_PAGE:(page + 1) * RESULTS_PER_PAGE]
       ]

    elif mode == 'slides':
        results = [
           dict(
               uuid = uuid,
               score = score,
               title = uuid,
               content = 'Text here with highlights',
               url = slides_index.get_url(uuid)
           )
           for score, uuid in sorted_scores[page * RESULTS_PER_PAGE:(page + 1) * RESULTS_PER_PAGE]
       ]
    return {
        'pageCount': num_results // RESULTS_PER_PAGE + (num_results % RESULTS_PER_PAGE > 0),
        'results': results,
    }


@Handler('/q/feedback', methods=['POST'], data_schema=Schema(cast=dict, schema={
    'query': Schema(cast=str, length=(3, 100)),
    'docs': Schema(cast=list, length=(0, 100),
                   schema=Schema(cast=str, regex='[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}')),
    'smart': Schema(cast=str, regex='([nlabL][ntp][ncub]){2}', optional=True, default='lncltc'),
}))
def feedback_get():
    """
    Retrieve most relevant terms from documents.
    """
    term_weights = feedback_terms(g.data['query'], g.data['docs'], g.data['smart'])

    sorted_term_weights = sorted(term_weights.items(), key=lambda x: x[1], reverse=True)[:10]

    return [dict(term=term, weight=weight) for term, weight in sorted_term_weights]
