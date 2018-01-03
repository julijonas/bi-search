import sys
import string
from itertools import groupby
import collections
import operator
import numpy as np
# from scipy import optimize
# import matplotlib.pyplot as plt
from operator import and_, or_
import itertools
import time
# import numpy as np
# import re
from .indexing import df as df_
from .indexing import tf as tf_
from .indexing import get_documents



inputs = [(1,"This is text number 1".split()),
(2,"This is text number 2".split()),
(3,"This is some more elaborate text".split()),
(4,"This is even much more elaborater that the rest text".split()),
(5,"This is most definitely my best one yet".split()),
(10,"Random words")]
#
# 
# 
# This need to be replace with the indexing one? 
def tokenize_string(s):
    return s.split()



class ProximityIndex():
    """
    Input is a list of tuples of the form:
        [ (document_id1 , ["word1",word2",..] ) ,  (document_id2 , ["word1",word2",..] ), ...]
    the words should already be stemmed and cleaned with the tokenizer
        
    Indexes the documents for proximity search.
    """
    def ld(self):
            return collections.defaultdict(list)
    def __init__(self,input,json=True):
        self.from_json= json
        if json:
            self.doc_ids = get_documents()
            return
        program_starts = time.time()


        index = collections.defaultdict(self.ld)
        self.doc_ids = set()
        for text in input:
            self.doc_ids.add(text[0])
            for i, word in enumerate(text[1]):
                index[word][text[0]].append(i)
        self.index = index

        now = time.time()
        print("INDEXING:: It has been {0} seconds since the loop started".format(now - program_starts)) 

        
    def tf(self,term,document,t="n",index=(None,None)):
        if not index[0] and self.from_json:
            tf = df_(term,document)
        else:
            ind = index[1] if index[1] else self.index
            doc_ids = index[0] if index[0] else self.doc_ids
            tf = len(ind[term][document])

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

    def idf(self,term,t="t",index=(None,None)):
        if not index[0] and self.from_json:
            df = tf_(term)
            N = len(self.doc_ids)
        else:

            ind = index[1] if index[1] else self.index
            doc_ids = index[0] if index[0] else self.doc_ids
            df = len(ind[term].keys())
            N = len(doc_ids)

        if t=="n":
            return 1
        if t=="t":
            return np.log10(N/df)
        if t=="p":
            return np.max([0,np.log10((N-df)/df)])
        return df

    def df(self,term):
        return len(self.index[term].keys())

    def cf(self,term):
        return sum([self.tf(term,x) for x in self.index[term].keys()]) 

    
    def w(self,term,document,t="ltc"):
        tf = self.tf(term,document,t[0])
        df = self.idf(term,t[1])
        N = len(self.doc_ids)
        return tf * df 
    
    def score(self,query,document,t="ltc"):
        query_terms = set(tokenize_string(query))
        # print (query_terms)
        if self.from_json:
            intersection = set([x for x in query_terms if df_(x,document) != 0])
        else:
            intersection = set([x for x in query_terms if self.index[x].get(document) != None])

        return sum([self.w(x,document,t) for x in intersection])
    
    
    def score_documents(self,query_terms,document,t="ltc"):
        
        scores = [self.score(term,document,t) for term in set(query_terms)]
        scores2 = [[term ,self.score(term,document,t)]   for term in set(query_terms)]
        tf_norm = 1
        if t[0]== "L":
            tf_norm =1 + np.log10(np.average([self.tf(term,document,"n") for term in set(query_terms)]))
        
        if t[0]== "a":
            tf_norm = np.max([self.tf(term,document,"n") for term in set(query_terms)])
        print ("tfnorm",tf_norm)
        norm = 1
        df_norm = 1
        if t[2]== "c":
            norm = 1/ np.linalg.norm(scores)
        scores = [x / tf_norm * norm * df_norm for x in scores]

        for x in scores2:
            x[1] = x[1]/ tf_norm * norm * df_norm 
        return scores ,scores2

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
    def cosin_score(self,query,document,T="ltclnc"):
        query_terms = (tokenize_string(query))

        qi_scores,qweights = self.score_query(query_terms,T[3:])
        di_scores,dweights =  self.score_documents(query_terms,document,T[:3])
        # print (qi_scores,qi_scores)
        
        assert len(qi_scores) == len(di_scores)
        s = np.dot(np.array(qi_scores),np.array(di_scores))
        norm = 1 #/ (np.linalg.norm(qi_scores) * np.linalg.norm(di_scores))
        v = s * norm 
        if not np.isnan(v): return v,dweights,qweights
        return 0,dweights,qweights
    
    def ranked_search_cos(self,term,SMART="ltclnc"):
        scores = [(self.cosin_score(term,d,SMART),d) for d in self.doc_ids]
        sorted_scores =  sorted(scores,reverse=True,key=lambda x: x[0][0])
        rankings = [(x[0][0],x[1]) for x in sorted_scores]
        return rankings, sorted_scores
    
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
            # "d_weights":d_weights
        }

        return r

def tfidf_test_instance(json):
    global inputs
    i = ProximityIndex(inputs,json)
    return i,inputs

if __name__ == "__main__":
    i = ProximityIndex(inputs)
    # For now :
        # the format is ddd.qqq
        #                                 tf    idf   Norm
        # for ddd, acceptable modes are [n,l,L][n,t,p][n,c] 
        # for qqq, acceptable modes are [n,l,L][n][n,c]
            # for ifd only n makes sense
    # x,_ = i.ranked_search_cos("This is is","ltclnc")
    # print ("ltclnc",x)
    # print ("ltcLnc",i.ranked_search_cos("This is is","ltcLnc"))
    # print ("ltcLnc",i.ranked_search_cos("This is not 1","ltcLnc"))

    print (i.search("This is weird","LtcLnc"))
