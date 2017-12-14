from . import Handler, Schema, g
from .indexing import *


@Handler('/tfidf/docs', methods=['GET'])
def tfidf_docs_get():
    return list(get_documents())


@Handler('/tfidf/tf/<token>', methods=['GET'], urla_schema=Schema(cast=dict, schema={
    "token": Schema(cast=str)
}))
def tfidf_tf_get():
    return "TF(%s) = %i"%(g.urla['token'], tf(g.urla['token']))


@Handler('/tfidf/df/<token>/<doc>', methods=['GET'], urla_schema=Schema(cast=dict, schema={
    "token": Schema(cast=str),
    "doc": Schema(cast=str)
}))
def tfidf_df_get():
    return "DF(%s, %s) = %i"%(g.urla['token'], g.urla['doc'], df(g.urla['token'], g.urla['doc']))
