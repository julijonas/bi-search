import json
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index_get():
    return Response("Server works fine, congrats!", status=200)


@app.route('/content', methods=['GET'])
def content_get():
    return Response(
        json.dumps(dict(server=['is', 'working'])),
        headers={'Content-Type': 'application/json'},
        status=200
    )


app.run(port=5000, debug=True)
