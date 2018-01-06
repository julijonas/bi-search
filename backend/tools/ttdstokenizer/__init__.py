import re
import Stemmer

# Prepare the token pattern
pattern = re.compile("(?P<word>([a-z0-9][a-z0-9\']+[a-z0-9])|[a-z0-9]+)")

# Load stop word list
with open('tools/ttdstokenizer/englishST.txt') as f:
    stop_words = set(tok.strip() for tok in f)


# Load Porter2 English stemmer
stemmer = Stemmer.Stemmer('english')
cache = {}


def tokenize(string):
    """
    Method is a generator of tokens found in the provided string.
    :param string: Query string
    :return: (token start location, token length, stemmed token)
    """
    # Iterate over found tokens:
    for m in re.finditer(pattern, string.lower()):
        tok = m.group("word")

        if tok not in stop_words:
            if tok not in cache:
                cache[tok] = stemmer.stemWord(tok)
            yield m.start(), len(tok), cache[tok]
