import math
from collections import Counter
from nltk.tokenize import word_tokenize
import numpy as np
from .preprocessor import preprocess


class Index:
    """Defines a TF-IDF index"""


    def __init__(self, tweets, dataset_size):
        self.df = {}
        self.total_vocab = []
        self.vocabulary_size = 0
        self.dataset_size = dataset_size
        self.D = None
        self.index = self.build_index(tweets)


    # TODO: External Merge Sort.
    #       Available Memory: M | Block Size: B
    #       M/B-way merge
    #       Ref: https://en.wikipedia.org/wiki/External_sorting
    def build_index(self, data):
        self.tweets = data
        self.preprocessed_text = [word_tokenize(str(preprocess(text))) for text in data]
        self.df = self.calculate_df(self.preprocessed_text, self.dataset_size)

        self.total_vocab = [x for x in self.df]
        self.vocabulary_size = len(self.df)

        tf_idf = self.calculate_tfidf(self.preprocessed_text, self.dataset_size, self.df)

        # Vectorize tf-idf
        self.D = np.zeros((self.dataset_size, self.vocabulary_size))
        for i in tf_idf:
            try:
                ind = self.total_vocab.index(i[1])
                self.D[i[0]][ind] = tf_idf[i]
            except:
                pass

        return tf_idf


    def search(self, k, query):
        preprocessed_query = preprocess(query)
        tokens = word_tokenize(str(preprocessed_query))

        d_cosines = []
        query_vector = self.gen_vector(tokens)

        for d in self.D:
            d_cosines.append(self.cosine_similarity(query_vector, d))

        out = np.array(d_cosines).argsort()[-k:][::-1]

        # NOTE: now this returns the relevant tweets' content
        return [self.tweets[idx] for idx in out]


    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


    def gen_vector(self, tokens):
        Q = np.zeros((len(self.total_vocab)))
        counter = Counter(tokens)
        words_count = len(tokens)

        for token in np.unique(tokens):
            tf = counter[token] / words_count
            self.df = self.doc_frequency(token)
            idf = math.log((self.dataset_size + 1) / (self.df + 1))

            try:
                ind = self.total_vocab.index(token)
                Q[ind] = tf * idf
            except:
                pass

        return Q


    def calculate_df(self, data, dataset_size):
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


    def doc_frequency(self, word):
        c = 0
        try:
            c = self.df[word]
        except:
            pass
        return c


    def calculate_tfidf(self, data, dataset_size, df):
        doc = 0
        tf_idf = {}
        for i in range(dataset_size):
            tokens = data[i]
            counter = Counter(tokens)
            words_count = len(tokens)

            for token in np.unique(tokens):
                tf = counter[token] / words_count
                df = self.doc_frequency(token)
                idf = np.log((dataset_size + 1) / (df + 1))
                tf_idf[doc, token] = tf * idf
            doc += 1
        return tf_idf
