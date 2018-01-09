from . import Handler, Schema, g, SMART_SCHEMA
from .rocchio import feedback_terms
from .tfidf import search_query
from .inverted_index import slides_index, pages_index
from . import get_preview


RESULTS_PER_PAGE = 18


def page_count(num_results):
    return num_results // RESULTS_PER_PAGE + (num_results % RESULTS_PER_PAGE > 0)


def get_items(collection, page):
    return collection[page * RESULTS_PER_PAGE:(page + 1) * RESULTS_PER_PAGE]


@Handler('/search/pages', methods=['POST'], data_schema=Schema(cast=dict, schema={
    'query': Schema(cast=str, length=(3, 100)),
    'smart': SMART_SCHEMA,
    'page': Schema(cast=int, bounds=(0, 100))
}))
def search_pages_post():
    scores, q_weights = search_query(pages_index, g.data['query'], g.data['smart'])
    result_count = len(scores)

    results = [
        dict(
            uuid=uuid,
            tfidf=d_weights,
            score=score,
            title=pages_index.get_title(uuid),
            preview=get_preview(uuid, g.data['query']),
            url=pages_index.get_url(uuid),
        )
        for score, uuid, d_weights in get_items(scores, g.data['page'])
    ]

    return dict(
        resultCount=result_count,
        pageCount=page_count(result_count),
        queryWeights=q_weights,
        results=results,
    )


@Handler('/search/slides', methods=['POST'], data_schema=Schema(cast=dict, schema={
    'query': Schema(cast=str, length=(3, 100)),
    'smart': SMART_SCHEMA,
    'page': Schema(cast=int, bounds=(0, 100))
}))
def search_slides_post():
    scores, q_weights = search_query(slides_index, g.data['query'], g.data['smart'])
    result_count = len(scores)

    results = [
        dict(
            uuid=uuid,
            tfidf=d_weights,
            score=score,
            url=slides_index.get_url(uuid),
        )
        for score, uuid, d_weights in get_items(scores, g.data['page'])
    ]

    return dict(
        resultCount=result_count,
        pageCount=page_count(result_count),
        queryWeights=q_weights,
        results=results,
    )


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
