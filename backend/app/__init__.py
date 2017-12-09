from flask import Flask, g, request, Response, render_template
from flask_cors import CORS
from .universal_handler import UniversalHandler
from time import time

app = Flask(__name__, template_folder='templates')
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


@Handler('/template_test', methods=['GET'])
def template_test_get():
    return render_template("template_test.html", stamp=int(time()))
