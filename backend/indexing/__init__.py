import sys
import os
import json
import io
import numpy as np
from tools.ttdstokenizer import tokenize
from scipy.sparse import lil_matrix, csr_matrix, save_npz


class IndexBuilder:
    def __init__(self):
        self._tokens = set()
        self._documents = set()
        self._metadata = dict()
        self._ii = dict()

    def add_to_index(self, uuid, content):
        self._documents.add(uuid)
        tokens = dict()
        self._ii[uuid] = tokens

        for _, _, token in tokenize(content['content']):
            tokens[token] = tokens.get(token, 0) + 1
            self._tokens.add(token)

        self._metadata[uuid] = dict(url=content['url'], title=content['title'])

    def dump(self, out_dir, name):
        tok_nums = {tok: num for tok, num in zip(self._tokens, range(len(self._tokens)))}
        doc_nums = {doc: num for doc, num in zip(self._documents, range(len(self._documents)))}
        nums_doc = {v: k for k, v in doc_nums.items()}
        nums_tok = {v: k for k, v in tok_nums.items()}

        print("Found tokens:", len(tok_nums))
        print("Found documents:", len(doc_nums))

        matrix = lil_matrix((len(doc_nums), len(tok_nums)), dtype=np.uint16)

        print("Matrixing: ")
        for doc in range(len(doc_nums)):
            docid = nums_doc[doc]
            for tok in range(len(tok_nums)):
                if tok in self._ii[docid]:
                    print(doc, tok, docid, nums_tok[tok])
                    matrix[doc, tok] = self._ii[docid][nums_tok[tok]]

        with io.open(os.path.join(out_dir, name + "_tok_nums.json"), mode="w", encoding="utf-8") as f:
            f.write(json.dumps(tok_nums, ensure_ascii=False))

        with io.open(os.path.join(out_dir, name + "_doc_nums.json"), mode="w", encoding="utf-8") as f:
            f.write(json.dumps(doc_nums, ensure_ascii=False))

        with io.open(os.path.join(out_dir, name + "_metadata.json"), mode="w", encoding="utf-8") as f:
            f.write(json.dumps(self._metadata, ensure_ascii=False))

        matrix = csr_matrix(matrix)

        save_npz(os.path.join(out_dir, name + "_ii"), matrix)


def build_index(in_dir, out_dir, silent=False):

    slides = IndexBuilder()
    pages = IndexBuilder()
    i = 0
    # Iterate over all subdirectories
    for dirName, subdirList, fileList in os.walk(in_dir):

        # Iterate over all files in the current subdirectory
        for fname in fileList:

            # Check that the file is a json file
            if fname.endswith(".json"):
                if not silent:
                    print("Adding %s" % fname)

                uuid = fname.split('.')[0]

                # Open the file with utf-8 encoding
                with io.open(os.path.join(dirName, fname), mode="r", encoding="utf-8") as f:

                    # Read the file into a dict
                    content = f.read()
                    content = json.loads(content)

                    # Add to the correct index.
                    if content['type'] == "slide":
                        if not silent:
                            print("\t--slide")
                        slides.add_to_index(uuid, content)
                    elif content['type'] == "page":
                        if not silent:
                            print("\t--page")
                        pages.add_to_index(uuid, content)
                    else:
                        print("UNKNOWN TYPE: " + content['type'])
            # if i > 10: break
            # i+=1
    slides.dump(out_dir, "slides")
    pages.dump(out_dir, "pages")