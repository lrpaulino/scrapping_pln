# -*- coding: utf-8 -*-

import pandas as pd
import nltk
import string

from unidecode import unidecode

df = pd.read_csv('data.csv', engine='c')

text = df['Text'].values[0]

ascii_lowercase = set(string.ascii_lowercase + ' ')
stemmer = nltk.stem.RSLPStemmer()
stopwords = nltk.corpus.stopwords.words('portuguese')
stopwords = {unidecode(x) for x in stopwords}
stopwords = {stemmer.stem(x) for x in stopwords}


def text_clean(text):
    text = text.strip()
    text = text.replace('\n', ' ')
    text = text.lower()
    text = unidecode(text)

    non_letters = filter(lambda c: c not in ascii_lowercase, set(text))
    for c in non_letters:
        text = text.replace(c, ' ')

    text = nltk.tokenize.word_tokenize(text)
    text = [stemmer.stem(x) for x in text]
    text = [x for x in text if x not in stopwords]

    return ' '.join(text)


df['Text'] = df['Text'].apply(text_clean)
df.to_csv('data_preprocessed.csv', index=False)
