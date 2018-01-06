import socket
from app import app
import sys

sys.path.append("tools")

host = "104.236.253.108" if socket.gethostname() == "ubuntu-512mb-nyc3-01" else "127.0.0.1"

app.run(host=host, port=5000, debug=True, threaded=True)
