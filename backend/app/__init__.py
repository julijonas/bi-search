from flask import Flask, g, request, Response
from flask_cors import CORS
from .universal_handler import UniversalHandler

app = Flask(__name__)
CORS(app)
Handler = UniversalHandler(app)


@Handler('/handler_test', methods=['GET'])
def handler_test_get():
    return [1, 4, 5, 7]


@Handler('/', methods=['GET'])
def index_get():
    return "Server works fine, congrats!"


@Handler('/content', methods=['GET'])
def content_get():
    return dict(server=['is', 'working'])