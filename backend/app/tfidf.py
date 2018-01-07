# import sys
# import string
# from itertools import groupby
import collections
# import operator
import numpy as np
# from scipy import optimize
# import matplotlib.pyplot as plt
# from operator import and_, or_
# import itertools
# import time
# import numpy as np
# import re
from tools.ttdstokenizer import tokenize
# from scipy.sparse import csr_matrix

inputs = [(1,"This is text number 1".split()),
(2,"This is text number 2".split()),
(3,"This is some more elaborate text".split()),
(4,"This is even much more elaborater that the rest text".split()),
(5,"This is most definitely my best one yet".split()),
(10,"Random words")]


class ProximityIndex:
    """
    Input is a list of tuples of the form:
        [ (document_id1 , ["word1",word2",..] ) ,  (document_id2 , ["word1",word2",..] ), ...]

    the words should already be stemmed and cleaned with the tokenizer

    Indexes the documents for proximity search.
    """


    def __init__(self, index):
        self._index = index
        self.N = len(index.get_documents())


    def ld(self):
            return collections.defaultdict(list)


    def tf(self, term, document, t="n", index=(None,None)):

        index = index[1] if index[1] else self.index
        tf = len(index[term][document])

        if t=="a":
            return 0.5 * tf
        if t=="n":
            return tf
        if t=="l":
            return (1 + np.log10(tf))
        if t== "b":
            return 1 if tf > 0 else 0
        if t=="L":
            return 1 + np.log10(tf)
        return

    def idf(self, term, t="t", index=(None,None)):

        doc_ids = index[0] if index[0] else self.doc_ids
        index = index[1] if index[1] else self.index

        df = len(index[term].keys())
        N = len(doc_ids)

        if t=="n":
            return 1
        if t=="t":
            return np.log10(N/df)
        if t=="p":
            return np.max([0,np.log10((N-df)/df)])
        return df

    def w(self,term,document,t="ltc"):
        tf = self.tf(term,document,t[0])
        df = self.idf(term,t[1])
        return tf * df

    def score_query(self,query_terms,t="lnc"):
        input = [(1,query_terms)]
        index = collections.defaultdict(self.ld)
        doc_ids = set()
        for text in input:
            doc_ids.add(text[0])
            for i, word in enumerate(text[1]):
                index[word][text[0]].append(i)
        args = (doc_ids,index)
        scores = [self.tf(term,1,t[0],args) * self.idf(term,t[1],args)   for term in set(query_terms)]
        scores2 = [[term ,self.tf(term,1,t[0],args)* self.idf(term,t[1],args)]   for term in set(query_terms)]

        # scaling
        tf_norm = 1
        if t[0]== "L":
            tf_norm = 1 + np.log10(np.average([self.tf(term,1,"n",args) for term in set(query_terms)]))

        if t[0]== "a":
            tf_norm = np.max([self.tf(term,1,"n",args) for term in set(query_terms)])

        norm = 1
        df_norm = 1
        if t[2]== "c":
            norm = 1/ np.linalg.norm(scores)
            norm = 1 if norm == np.inf else norm
        scores = [x / tf_norm * norm * df_norm for x in scores]
        for x in scores2:
            x[1] = x[1]/tf_norm * norm * df_norm

        return scores,scores2

    def score_documents(self,query_terms,SMART):

         # Get all term frequencies [doc x terms]
        tf_all = self._index[:,query_terms].todense()
        # apply normalizations to tf
        if SMART[0] == "l":
            tf_all = 1 + np.log(tf_all)
        if SMART[0] == "n":
            pass
            # tf_all *= 1
        if SMART[0] == "a":
            max_tf = np.max(tf_all,axis= 0)
            tf_all = 0.5 + (0.5)  * tf_all / np.max(tf_all,axis=0)

        if SMART[0] == "b":
            tf_all = 1* (tf_all > 0)

        if SMART[0] == "L":
            tf_all = (1 + np.log10(tf_all) ) / (1 + np.log10(np.average(tf_all,axis=1)))
        


        # Get df for all terms [1 x terms]
        df_all = np.sum(self._index[:,query_terms] > 0,axis=0)
        # Stack for all docs [doc x terms]
        df_all = np.vstack([df_all]* tf_all.shape[0])


        # apply normalizations to df 
        if SMART[1] == "n":
            df_all = np.ones_like(df_all)

        if SMART[1] == "t":
            df_all = (self.N * np.ones_like(df_all))/ df_all
            df_all = np.log(df_all)
        
        if SMART[1] == "p":
            df_all = np.vstack([np.zeros_like(df_all),df_all])
            df_all = np.max(df_all,axis=0)
        
        # Documents tf_idf for each token
        documents_tf_idf = np.matrix(np.multiply(tf_all,df_all))

        return documents_tf_idf 

    def ranked_search_cos(self,term,SMART="ltclnc"):
        # NEw stuff here
        query_terms = list(tokenize(term, True))

        documents_tf_idf = self.score_documents(query_terms,SMART)

        # Query Scores only calculated once
        qi_scores,qweights = self.score_query(query_terms,SMART[3:])
        query_tf_if = np.array(qi_scores).reshape((len(qi_scores), 1))
        
        # Compute scores
        cosine_scores = documents_tf_idf.dot(query_tf_if)

        
        cosine_scores = (np.array(cosine_scores)[:,0])
        sorted_scores = np.sort(cosine_scores)[::-1]
        sorted_doc_nums = np.argsort(cosine_scores)[::-1]
        
        dweights = documents_tf_idf[sorted_doc_nums,:]

        sorted_doc_ids = self._index.nums_to_docs(sorted_doc_nums)

        rankings = list(zip(sorted_scores,sorted_doc_ids))

        
        d_weights = {}
        for i,d in enumerate(rankings):
            uuid = d[1]
            w = dweights[i,:]
            term_weights = {}
            for j,t in enumerate(query_terms):
                term_weights[t] = w[0,j]
            d_weights[uuid] = term_weights

        return rankings, (qweights,d_weights)

    def search(self,term,SMART="ltcLnc"):

        rankings, sorted_with_w = self.ranked_search_cos(term,SMART)
        q_weights = { k:{"query":v, "documents":[], } for k,v in sorted_with_w[0][0][2] }


        d_weights = {}
        for results,doc_id in sorted_with_w:
            d_weights[doc_id] = results[1]
            for word,score in results[1]:
                if np.isnan(score):
                    pass
                else:
                    q_weights[word]["documents"] += [score]

        for k in q_weights.keys():
            doc_scores = q_weights[k]["documents"]

            q_weights[k]["doc_total"] = np.sum(doc_scores)
            found_in_ = len(list(filter(lambda x: x>0,doc_scores)))
            q_weights[k]["documents"] = found_in_
            q_weights[k]["doc_average"] = np.sum(doc_scores) / found_in_
        r = {
            "rankings":rankings,
            "q_weights":q_weights,
            "d_weights":d_weights
        }

        return r

def tfidf_test_instance(json):
    global inputs
    i = ProximityIndex(inputs, json)
    return i,inputs


def search_query(index, query, smart):
    proximity_index = ProximityIndex(index)
    rankings, sorted_scores = proximity_index.ranked_search_cos(query, smart)
    return rankings
