import re
import stemming.porter2 as stemmer

# Prepare the token pattern
pattern = re.compile("(?P<word>([\@\#]?[a-z0-9][a-z0-9\']+[a-z0-9])|[a-z0-9]+)")



def tokenize(string):
    """
    Method is a generator of tokens found in the provided string.
    :param string: Query string
    :return: (token start location, token length, stemmed token)
    """
    # Iterate over found tokens:
    for m in re.finditer(pattern, string.lower()):
        tok = m.group("word")
        yield m.start(), len(tok), stemmer.stem(tok)
