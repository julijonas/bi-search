import os
import json
from .inverted_index import InvertedIndex

# Tf and df are the wrong way around
# if anyone cjanges them let me know to change mine too
# xx
# -Stephanos


slides_index = InvertedIndex(os.environ['TTDS_INDEX_LOCATION'], "slides")
pages_index = InvertedIndex(os.environ['TTDS_INDEX_LOCATION'], "pages")
