import os
from flask import Flask, g, request, Response, render_template
from flask_cors import CORS


app = Flask(__name__, template_folder='templates',
            static_folder=os.path.join(os.environ['TTDS_SCRAPE_LOCATION'], "slides"), static_url_path='/static/thumbs')
CORS(app)

# Import infrastructure now that the app has been created.
from .infrastructure import *

# Create the Handler for all API calls.
Handler = UniversalHandler(app)


SMART_SCHEMA = Schema(cast=str, regex='([nlabL][ntp][ncub]){2}', optional=True, default='lncltc')


# Register validation handlers

@app.errorhandler(ValidationException)
def validation_error_handler(e):
    return Response(render_template('400.html', message=str(e)), status=400)


# Import functionality now that everything was set up properly.
from .highlighting import *
from .inverted_index import *
from .query_endpoints import *
