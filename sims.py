# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 09:40:30 2019

@author: Mengyu Liu
"""
from gensim import corpora, models, similarities
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
documents = ["Shipment of gold damaged in a fire", "Delivery of silver arrived in a silver truck","Shipment of gold arrived in a truck"]
texts = [[word for word in document.lower().split()] for document in documents]
print(texts)
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
lsi.print_topics(2)
corpus_lsi = lsi[corpus_tfidf]
for doc in corpus_lsi:
    print(doc)
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=2)
lda.print_topics(2)
index = similarities.MatrixSimilarity(lsi[corpus])
query = "gold silver truck"
query_bow = dictionary.doc2bow(query.lower().split())
query_lsi = lsi[query_bow]
print (query_lsi)
sims = index[query_lsi]
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
print (sort_sims)