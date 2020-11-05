from nltk.tokenize import word_tokenize
from preprocessor import preprocess
import math
import numpy as np
from collections import Counter


# TODO: refactor as class


def calculate_df(data, dataset_size):
    df = {}
    for i in range(dataset_size):
        tokens = data[i]
        for w in tokens:
            try:
                df[w].add(i)
            except: 
                df[w] = {i}

    # Replace list of ids with count of documents
    for i in df:
        df[i] = len(df[i])

    return df


def doc_frequency(word):
    c = 0
    try:
        c = df[word]
    except:
        pass
    return c


def calculate_tfidf(data, dataset_size, df):
    doc = 0
    tf_idf = {}
    for i in range(dataset_size):
        tokens = data[i]
        counter = Counter(tokens)
        words_count = len(tokens)

        for token in np.unique(tokens):
            tf = counter[token] / words_count
            df = doc_frequency(token)
            idf = np.log((dataset_size + 1) / (df + 1))
            tf_idf[doc, token] = tf * idf
        doc += 1
    return tf_idf


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def gen_vector(tokens):
    Q = np.zeros((len(total_vocab)))
    counter = Counter(tokens)
    words_count = len(tokens)

    for token in np.unique(tokens):
        tf = counter[token] / words_count
        df = doc_frequency(token)
        idf = math.log((dataset_size + 1) / (df + 1))

        try:
            ind = total_vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass

    return Q


def search(k, query):
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))

    d_cosines = []
    query_vector = gen_vector(tokens)

    for d in D:
        d_cosines.append(cosine_similarity(query_vector, d))

    out = np.array(d_cosines).argsort()[-k:][::-1]
    return out


def build_index(data, size):
    global df
    global total_vocab
    global vocabulary_size
    global dataset_size
    global D
    dataset_size = size

    preprocessed_text = [word_tokenize(str(preprocess(text))) for text in data]
    df = calculate_df(preprocessed_text, dataset_size)

    total_vocab = [x for x in df]
    vocabulary_size = len(df)
    print('Vocabulary size:', vocabulary_size)

    tf_idf = calculate_tfidf(preprocessed_text, dataset_size, df)

    # Vectorize tf-idf
    D = np.zeros((dataset_size, vocabulary_size))
    for i in tf_idf:
        try:
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = tf_idf[i]
        except:
            pass

    return tf_idf
