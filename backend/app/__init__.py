from time import time

from flask import Flask, g, request, Response, render_template
from flask_cors import CORS

from .universal_handler import UniversalHandler
from .tfidf import tfidf_test_instance
from .validation import ValidationException, Schema, raw_json
from .indexing import slides_index


app = Flask(__name__, template_folder='templates')
CORS(app)
Handler = UniversalHandler(app)


SMART_SCHEMA = Schema(cast=str, regex='([nlabL][ntp][ncub]){2}', optional=True, default='lncltc')


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


@Handler('/tfidf_test', methods=['GET'], args_schema=Schema(cast=dict, schema={
    "q": Schema(cast=str, length=(3,128)),
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
    i,test_documents = tfidf_test_instance(True)

    # Return dict as json
    return json.dumps(i.search(g.args['q'], g.args['smart']))


@Handler('/validation/<stuff>', methods=['GET'], args_schema=Schema(cast=dict, schema={
    "a": Schema(cast=int, bounds=(0, 10), optional=True, default=8),
    "b": Schema(cast=int, bounds=(0, 10), optional=True, force_present=True),
    "list": Schema(cast=raw_json, schema=Schema(cast=list, schema=Schema(cast=int)))
}), urla_schema=Schema(cast=dict, schema={
    "stuff": Schema(cast=str, length=(3, 16))
}))
def validation_get():
    print(g.args)
    print(g.urla)
    return "All arguments passed validation"


from .indexing import *
from .tfidf_endpoints import *
from .query_endpoints import *
