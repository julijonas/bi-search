import os
import io
import json
from .. import Handler, render_template, app, g
from .. import Schema
from tools.ttdstokenizer import tokenize


def simple_highlights(content, query):
    tokens = set(tokenize(query, True))
    snippets = list()
    found = set()
    for start, length, token in tokenize(content):
        if token in tokens:
            snippets.append(content[max(0, start - 30) : min(len(content), start + length + 30)])
            found.add(content[start:start+length])
    return dict(preview=" ... ".join(snippets), highlight=list(found))


def get_preview(uuid, query):
    path = os.path.join(app.static_folder, "pages", uuid + ".json")
    if os.path.exists(path):
        with io.open(path, 'r', encoding='utf-8') as f:
            s = json.loads(f.read())['content']
            return simple_highlights(s, query)
    return None


@Handler('/highlight', methods=['GET'])
def highlights_get():
    return render_template('highlight_get.html')


@Handler('/highlight', methods=['POST'], data_schema=Schema(cast=dict, schema={
    'document': Schema(cast=str),
    'query': Schema(cast=str)
}))
def highlights_post():
    return get_preview(g.data['document'], g.data['query'])
