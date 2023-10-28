import re
from collections import Counter
import spacy
import en_core_web_trf
nlp = en_core_web_trf.load()
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

with open("english.txt") as file:
    lines = [line.rstrip() for line in file]

stop_words = set(lines)

#stop_words = set(stopwords.words("english"))
stop_words.add("hourglass")
def preprocess(input_sentence):
    input_sentence = input_sentence.lower()
    input_sentence = re.sub(r'[^\w\s]','',input_sentence)
    tokens = word_tokenize(input_sentence)
    input_sentence = [i for i in tokens if not i in stop_words]
    return(input_sentence)

def compare_overlap(user_message, possible_response):
    similar_words = 0
    for token in user_message:
        if token in possible_response:
              similar_words += 1
    return similar_words
  
def extract_nouns(tagged_message):
    message_nouns = list()
    for token in tagged_message:
        if token[1].startswith("N"):
            message_nouns.append(token[0])
    return message_nouns

def compute_similarity(tokens, category):
    output_list = list()
    for token in tokens:
        output_list.append([token.text, category.text, token.similarity(category)])
    return output_list
  