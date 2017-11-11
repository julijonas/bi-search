from flask import Flask, Response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_get():
    return Response("Server works fine, congrats!", status=200)


app.run(port=5000, debug=True)