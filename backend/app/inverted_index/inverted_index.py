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

        with io.open(os.path.join(index_dir, index_name + "_metadata.json"), mode="r", encoding="utf-8") as f:
            self._metadata = json.loads(f.read())

        self._matrix = load_npz(os.path.join(index_dir, index_name + "_ii.npz"))

        self._nums_doc = {v: k for k, v in self._doc_nums.items()}
        self._nums_tok = {v: k for k, v in self._tok_nums.items()}

    def tf(self, token, document):
        """
        DON'T USE THIS ANYMORE!
        :param token: Don't even think about it.
        :param document: Don't even think about it.
        :return: Nothing at all..
        """
        if token not in self._tok_nums:
            return 0
        if document not in self._doc_nums:
            return 0
        tok_num = self._tok_nums[token]
        doc_num = self._doc_nums[document]

        return self._matrix[doc_num, tok_num]

    def df(self, token):
        """
        DON'T USE THIS ANYMORE!
        :param token: Don't even think about it.
        :return: Nothing at all..
        """
        if token not in self._tok_nums:
            return 0
        token_column = self._matrix[:, self._tok_nums[token]]
        return np.sum(token_column.T * (token_column > 0))

    def get_url(self, document):
        """
        Returns the URL of the requested document.
        :param document: Document ID (GUID)
        :return: Url of the document (string). None if the document is not known.
        """
        if document in self._metadata:
            return self._metadata.get(document, None)['url']
        return None

    def get_documents(self):
        """
        :return: A set of all document ids.
        """
        return self._doc_nums.keys()

    def docs_to_nums(self, docs):
        """
        Converts a list of document IDs to their corresponding row numbers in the inverted index matrix.
        :param docs: Document IDs (GUIDs)
        :return: Row numbers (integers)
        """
        return [self._doc_nums[d] for d in docs if d in self._doc_nums]

    def toks_to_nums(self, toks):
        """
        Converts a list of tokens to their corresponding column numbers in the inverted index matrix.
        :param docs: Tokens (strings)
        :return: Column numbers (integers)
        """
        return [self._tok_nums[t] for t in toks if t in self._tok_nums]

    def nums_to_docs(self, nums):
        """
        Converts the row numbers of the inverted index matrix to their corresponding document IDs.
        :param nums: Row numbers (integers)
        :return: Document IDs (GUIDs)
        """
        return [self._nums_doc[n] for n in nums if n in self._nums_doc]

    def nums_to_toks(self, nums):
        """
        Converts the column numbers of the inverted index matrix to their corresponding tokens.
        :param nums: Column numbers (integers)
        :return: Tokens (strings)
        """
        return [self._nums_tok[n] for n in nums if n in self._nums_tok]

    def __getitem__(self, item):
        """
        Returns the selected rows and columns of the inverted index matrix.
        Element at row i, column j is the amount of times token j appeared in document i.
        Rows are documents, columns are tokens. Example usage:
        >>> i = InvertedIndex('path', 'name')
        >>> _ = i[45, 78] # Document 45, token 78
        >>> _ = i[97, "hello"] # Document 45, token "hello"
        >>> _ = i[4:7, :] # Documents 4 through 7, all tokens
        >>> _ = i[['uuid1', 'uuid2', 'uuid3'], :] # Documents uuid1, uuid2, uuid3, all tokens.
        :param item: See example usage
        :return: Matrix slice.
        """
        assert (type(item) is tuple)
        assert (len(item) == 2)
        item0 = item[0]
        item1 = item[1]

        if type(item0) is str:
            item0 = self._doc_nums.get(item0, 0)
        if type(item1) is str:
            item1 = self._tok_nums.get(item1, 0)
        if type(item0) is list and type(item0[0]) is str:
            item0 = self.docs_to_nums(item0)
        if type(item1) is list and type(item1[0]) is str:
            item1 = self.toks_to_nums(item1)

        return self._matrix[item0, item1]



