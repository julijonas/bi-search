import os
import re
import json
import stemming.porter2 as stemmer


INDEX = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ii.json")))


def get_documents():
    generator = list(set(INDEX[t].keys()) for t in INDEX.keys())
    print(INDEX.keys())
    return set.union(*generator)


# Tf and df are the wrong way around 
# if anyone cjanges them let me know to change mine too 
# xx
# -Stephanos

def tf(token):
    if token not in INDEX:
        return 0
    return len(INDEX[token].keys())


def df(token, document):
    if token not in INDEX:
        return 0
    if document not in INDEX[token]:
        return 0
    return INDEX[token][document]

def tdf(token):
    if token not in INDEX:
        return 0
    return len(INDEX[token])



# Prepare the token pattern
pattern = re.compile("(?P<word>([\@\#]?[a-z0-9][a-z0-9\']+[a-z0-9])|[a-z0-9]+)")



def tokenize(string):
    """
    Method is a generator of tokens found in the provided string.
    :param string: Query string
    :return: Tokens one by one
    """
    # Iterate over found tokens:
    for m in re.finditer(pattern, string.lower()):
        tok = m.group("word")
        yield stemmer.stem(tok)


def add_to_index(index, location):
    j = json.load(open(location))
    guid = os.path.split(location)[-1].split(".")[0]

    for token in tokenize(j['content']):
        if token not in index:
            index[token] = dict()
        if guid not in index[token]:
            index[token][guid] = 0
        index[token][guid] += 1


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    index = dict()
    for dirName, subdirList, fileList in os.walk(os.path.join(dir_path, "resources")):
        for fname in fileList:
            print("Tokenizing %s" % fname)
            add_to_index(index, os.path.join(dirName, fname))
    with open("ii.json", "w") as f:
        json.dump(index, f)
