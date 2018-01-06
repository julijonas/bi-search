import os
from .. import Handler, render_template
from ..validation import Schema, raw_json


@Handler('/highlight', methods=['GET'])
def highlights_get():
    return render_template('highlight_get.html')


@Handler('/highlight', methods=['PSOT'], data_schema=Schema(cast=dict, schema={
    'document': Schema(cast=str),
    'query': Schema(cast=str)
}))
def highlights_post():
    return render_template('highlight_get.html')