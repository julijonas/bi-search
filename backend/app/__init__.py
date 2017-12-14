from flask import Flask, g, request, Response, render_template
from flask_cors import CORS
from .universal_handler import UniversalHandler
from time import time
from .validation import ValidationException, Schema, raw_json


app = Flask(__name__, template_folder='templates')
CORS(app)
Handler = UniversalHandler(app)


@app.errorhandler(ValidationException)
def validation_error_handler(e):
    return Response(render_template('400.html', message=str(e)), status=400)


@Handler('/handler_test', methods=['GET'])
def handler_test_get():
    return [1, 4, 5, 7]


@Handler('/', methods=['GET'])
def index_get():
    return "Server works fine, congrats!"


@Handler('/content', methods=['GET'])
def content_get():
    return dict(server=['is', 'working'])


@Handler('/template_test', methods=['GET'])
def template_test_get():
    return render_template("template_test.html", stamp=int(time()))


@Handler('/validation/<stuff>', methods=['GET'], args_schema=Schema(cast=dict, schema={
    "a": Schema(cast=int, bounds=(0, 10), optional=True, default=8),
    "list": Schema(cast=raw_json, schema=Schema(cast=list, schema=Schema(cast=int)))
}), urla_schema=Schema(cast=dict, schema={
    "stuff": Schema(cast=str, length=(3, 16))
}))
def validation_get():
    print(g.args['a'], g.urla['stuff'])
    print(g.args['list'])
    return "All arguments passed validation"


from .indexing import *
from .tfidf_endpoints import *
