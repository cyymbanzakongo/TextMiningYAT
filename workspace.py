import pandas as pd
from pathlib import Path
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector


def get_detector(nlp, name):
    # https://stackoverflow.com/questions/66712753/how-to-use-languagedetector-from-spacy-langdetect-package
    return LanguageDetector()


def process(file):
    df = pd.read_csv(file)
    n = 0
    print(df.head())
    for x in df['Label'].values:
        if x == 1:
            n += 1
    print(n)  # 13484
    print(len(df) - n)  # 39708


in_file = Path.cwd() / 'tweets_no_duplicates.csv'

def ret():
    df = pd.read_csv(in_file)
    tweets_list = df['Text'].values
#    tweets_list = df.iloc[:, 1].values[-10:] #iloc selecting all rows, then second column only
    nlp = spacy.load('en_core_web_sm', exclude=[
                     'ner', 'tok2vec', 'lemmatizer', 'senter', 'attribute-ruler'])  # exclude all for faster performance
    # i still dont entirely understand the language object, got code from: https://stackoverflow.com/questions/66712753/how-to-use-languagedetector-from-spacy-langdetect-package
    Language.factory('lang-detect', func=get_detector)
    nlp.add_pipe('lang-detect', last=True)
    langs_lst = [doc._.language['language'] for doc in [nlp(
        tweet) for tweet in tweets_list]]  # nested list comprehension of spacy pipeline
    df.insert(4, 'lang', langs_lst)  # insert column at last index point
    df_fltrd = df[df['lang'] == 'en']  # new filtered dataframe from old one
    df_fltrd.to_csv('./dbs/tweets_fltrd.csv')


def ret2():
    df = pd.read_csv(in_file)
    print(df["Label"].value_counts())
