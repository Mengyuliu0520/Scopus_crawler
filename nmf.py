

from __future__ import print_function
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import pandas as pd
from scipy.spatial.distance import cdist as cdi
n_samples = 2000
n_features = 100
n_components = 10
n_top_words = 20

doc = pd.read_csv('second_result.csv')
manu = pd.read_csv('all2012.csv')
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


# filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

print("Loading dataset...")
t0 = time()
#data_samples = dataset.data[:n_samples]
data_samples = doc['abstract']
manu_text = manu['original_abstruct_text']
print(type(data_samples))
print(type(manu_text))
dl = pd.Series.tolist(data_samples)
ml = pd.Series.tolist(manu_text)
mix = ml+dl
print("done in %0.3fs." % (time() - t0))

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   max_features=n_features,
                                   stop_words='english')
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(mix)
length = len(manu['original_abstruct_text'])
print("size:  ")
print(tfidf.shape)
print("done in %0.3fs." % (time() - t0))


# Fit the NMF model
#print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
#      "n_samples=%d and n_features=%d..."
#      % (n_samples, n_features))
#t0 = time()
#nmf = NMF(n_components=n_components, random_state=1,
#          alpha=.1, l1_ratio=.5).fit(tfidf)
#print("done in %0.3fs." % (time() - t0))
#
#print("\nTopics in NMF model (Frobenius norm):")
#tfidf_feature_names = tfidf_vectorizer.get_feature_names()
#print_top_words(nmf, tfidf_feature_names, n_top_words)

# Fit the NMF model
print("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
      "tf-idf features, n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))
print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)
review_topic = nmf.fit_transform(tfidf)
mt = review_topic[:length,:]
rt = review_topic[length+1:,:]
res = cdi(mt,rt)
print(res.shape)








