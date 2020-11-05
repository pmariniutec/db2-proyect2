import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from num2words import num2words
import numpy as np


def lower_case(data):
    return np.char.lower(data)


def remove_stopwords(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_txt = ''
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_txt = f'{new_txt} {w}'
    return new_txt


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
    data = np.char.replace(data, ',', '')
    return data


def remove_apostrophe(data):
    return np.char.replace(data, "'", '')


def stemming(data):
    stemmer = PorterStemmer()
    tokens = word_tokenize(str(data))
    new_txt = ''
    for w in tokens:
        new_txt = f'{new_txt} {stemmer.stem(w)}'
    return new_txt


def numbers_to_text(data):
    tokens = word_tokenize(str(data))
    new_txt = ''
    for w in tokens:
        try:
            w = num2words(int(w))
        except Exception as e:
            pass
        new_txt = f'{new_txt} {w}'
    new_txt = np.char.replace(new_txt, '-', '')
    return new_txt


def preprocess(data):
    data = lower_case(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
    data = remove_stopwords(data)
    data = numbers_to_text(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = numbers_to_text(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = remove_stopwords(data)
    return data
