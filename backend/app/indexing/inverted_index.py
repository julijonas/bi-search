import io
import os
import json
import numpy as np
from scipy.sparse import load_npz

class InvertedIndex:
    def __init__(self, index_dir, index_name):

        with io.open(os.path.join(index_dir, index_name + "_tok_nums.json"), mode="r", encoding="utf-8") as f:
            self._tok_nums = json.loads(f.read())

        with io.open(os.path.join(index_dir, index_name + "_doc_nums.json"), mode="r", encoding="utf-8") as f:
            self._doc_nums = json.loads(f.read())

        self._matrix = load_npz(os.path.join(index_dir, index_name + "_ii.npz"))


        self._nums_doc = {v: k for k, v in self._doc_nums.items()}
        self._nums_tok = {v: k for k, v in self._tok_nums.items()}


    def tf(self, token, document):
        if token not in self._tok_nums:
            return 0
        if document not in self._doc_nums:
            return 0
        tok_num = self._tok_nums[token]
        doc_num = self._doc_nums[document]

        return self._matrix[doc_num, tok_num]


    def df(self, token):
        if token not in self._tok_nums:
            return 0
        token_column = self._matrix[:, self._tok_nums[token]]
        return np.sum(token_column.T * (token_column > 0))

    def get_documents(self):
        return self._doc_nums.keys()

    def docs_to_nums(self, docs):
        return [self._doc_nums[d] for d in docs if d in self._doc_nums]

    def toks_to_nums(self, toks):
        return [self._tok_nums[t] for t in toks if t in self._tok_nums]

    def nums_to_docs(self, nums):
        return [self._nums_doc[n] for n in nums if n in self._nums_doc]

    def nums_to_toks(self, nums):
        return [self._nums_tok[n] for n in nums if n in self._nums_tok]

    def __getitem__(self, item):
        assert (type(item) is tuple)
        assert (len(item) == 2)
        item0 = item[0]
        item1 = item[1]

        if type(item0) is list and type(item0[0]) is str:
            item0 = self.docs_to_nums(item0)
        if type(item1) is list and type(item1[0]) is str:
            item1 = self.toks_to_nums(item1)

        return self._matrix[item0, item1]



