# !/usr/bin/env python3
"""
Compares sentences by using vector representation and
sklearn's cosine_similarity to create a similarity matrix

Author: James Rose
"""
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import networkx
import multiprocessing as mp
import warnings
warnings.filterwarnings("ignore")
glove = open('WordEmbeddings.txt', encoding='utf-8')  # Load to RAM, file is 300mb, so only want to have to read once
embeddings = {}
for values in glove:
    word = values[0]
    embeddings[word] = np.asarray(values.split()[1:], dtype='float32')
glove.close()


def remove_stopwords(sentence):
    stop_words = stopwords.words('english')
    new_sentence = " ".join([word for word in sentence.split(" ") if word not in stop_words])
    return new_sentence


def rank(article_text, keep_score=False):
    sentences = []
    for s in article_text.split(". "):
        sentences.append(sent_tokenize(s))
    sentences = [y for x in sentences for y in x] # flatten list
    # Keep only alpha
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    # make lowercase
    clean_sentences = [s.lower() for s in clean_sentences]
    # remove stop words
    clean_sentences = [remove_stopwords(r) for r in clean_sentences]
    sentence_vectors = []
    # Vector representation
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([embeddings.get(w, np.zeros((100,))) for w in i.split()]) / (len(i.split()) + 0.00001)
        else:
            v = np.zeros((100,))
        if isinstance(v, np.ndarray):
            sentence_vectors.append(v)
    # creating similarity matrix
    sim_mat = np.zeros([len(sentences), len(sentences)])  # empty matrix
    for i in range(len(sentence_vectors)):
        for j in range(len(sentence_vectors)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, 100),
                                                  sentence_vectors[j].reshape(1, 100)
                                                  )[0, 0]
    nx = networkx.from_numpy_array(sim_mat)
    scores = networkx.pagerank(nx)
    ranked_sentences = sorted(((scores[ind], sentence) for ind, sentence in enumerate(sentences)), reverse=True)
    if keep_score:
        return ranked_sentences
    else:
        return [ranked[1] for ranked in ranked_sentences]

if __name__ == "__main__":
    test = "Hello world, what a wonderful day it is. I hope you are enjoying such a lovely day. The Sun is bright" \
           " and shinning its rays of happiness. Hopefully your are not sitting inside typing this sentences like me!"
    print(rank(test))