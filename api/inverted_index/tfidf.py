import math
from collections import Counter
from nltk.tokenize import word_tokenize
import numpy as np
from .preprocessor import preprocess
from .twitter_serializer import get_tweets_by_ids


class Index:
    """Defines a TF-IDF index"""


    def __init__(self, tweets, dataset_size):
        self.df = {}
        self.total_vocab = []
        self.vocabulary_size = 0
        self.dataset_size = dataset_size
        self.D = None
        self.index = self.build_index(tweets)


    def build_index(self, documents):
        # For the corpus, we only store the tweet ID
        self.corpus = list(map(lambda x: x.get('id'), documents))
        preprocessed_text = [word_tokenize(str(preprocess(item.get('text')))) for item in documents]
        self.df = self.calculate_df(preprocessed_text, self.dataset_size)

        self.total_vocab = [x for x in self.df]
        self.vocabulary_size = len(self.df)

        tf_idf = self.calculate_tfidf(preprocessed_text, self.dataset_size, self.df)

        # Vectorize tf-idf
        self.D = np.zeros((self.dataset_size, self.vocabulary_size))

        for i in tf_idf:
            try:
                ind = self.total_vocab.index(i[1])
                self.D[i[0]][ind] = tf_idf[i]
            except:
                pass

        # Cache document norms
        self.norms = [np.linalg.norm(d) for d in self.D]

        return tf_idf

    def add_documents(self, documents):
        self.corpus.extend(map(lambda x: x.get('id'), documents))

        preprocessed_text = [word_tokenize(str(preprocess(item.get('text')))) for item in documents]
        dataset_size = len(preprocessed_text)
        self.dataset_size += dataset_size

        preprocessed_text.extend(preprocessed_text)
        df = self.calculate_df(preprocessed_text, dataset_size)
        self.df = df

        total_vocab = [x for x in df]
        self.total_vocab.extend(total_vocab)
        vocabulary_size = len(df)
        self.vocabulary_size += vocabulary_size

        tf_idf = self.calculate_tfidf(preprocessed_text, dataset_size, df)

        # Vectorize tf-idf
        D = np.zeros((dataset_size, vocabulary_size))
        self.D = np.append(self.D, D)

        for i in tf_idf:
            try:
                ind = total_vocab.index(i[1])
                self.D[i[0]][ind] = tf_idf[i]
            except:
                pass

        # Cache document norms
        norms = [np.linalg.norm(d) for d in D]
        self.norms.append(norms)

        self.index.update(tf_idf)


    def search(self, k, query):
        preprocessed_query = preprocess(query)
        tokens = word_tokenize(str(preprocessed_query))

        d_cosines = []
        query_vector = self.gen_vector(tokens)

        idx = 0
        for d in self.D:
            d_cosines.append(self.cosine_similarity(query_vector, d, self.norms[idx]))
            idx += 1

        out = np.array(d_cosines).argsort()[-k:][::-1]

        doc_ids = [self.corpus[idx] for idx in out]
        return get_tweets_by_ids(doc_ids)



    def cosine_similarity(self, a, b, norm_b):
        return np.dot(a, b) / (np.linalg.norm(a) * norm_b)


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
