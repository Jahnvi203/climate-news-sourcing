import json
from datetime import datetime
from dateutil.tz import gettz
from urllib.parse import quote_plus
from flask import Flask, request, jsonify
from dateutil import parser

from settings import *
import requests
from invokes import invoke_http
from requests.exceptions import RequestException
import pandas as pd


from flask_cors import CORS

import asyncio

import os
import sys

import jsonlines

import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import nltk
import spacy
import gensim
import pytextrank
import re
from transformers import pipeline
from bs4 import BeautifulSoup

# Add requirements for summarisation
from collections import defaultdict
from collections import Counter
from nltk.corpus import wordnet
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tag import pos_tag
from heapq import nlargest
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
import sentencepiece

####################################

nltk.download('words')
# Initialise Lemmatizer
lemmatizer = WordNetLemmatizer()
STOPS = set(stopwords.words('english'))

rank_URL = "http://localhost:5002/rank"

app = Flask(__name__)
CORS(app)

goo_key = os.environ.get('goo_key')
goo_id = os.environ.get('goo_id')
COUNTRY = os.environ.get('COUNTRY')



# db = SQLAlchemy(app)

# db.metadata.clear()

def lemmatize(text):
    text = text.lower()
    text =  re.sub("[^a-zA-Z]", " ", text).split()    
    meaningful_words = [w for w in text if w not in STOPS]
    meaningful_words = [lemmatizer.lemmatize(w) for w in meaningful_words]
    return (" ".join(meaningful_words))
# Helper function -Search


def lemmatize_ner(text):
    text = re.sub("[^a-zA-Z]", " ", text).split()
    meaningful_words = [w for w in text if w not in STOPS]
    meaningful_words = [lemmatizer.lemmatize(w) for w in meaningful_words]
    return (" ".join(meaningful_words))
    

# Helper Function to preprocess 
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("textrank")

def basic_preprocess_keepstopwords(self_text):
     # 1. Remove html tags
    words = BeautifulSoup(self_text, features="html.parser").get_text()
    # print("Before: ", words)
    # 2. Convert words to lower case and split each word up
    words = self_text.lower()
    doc = nlp(words)
    # 3. Remove non-letters aka punctuation
    # MIGHT NOT DO AS IT WILL AFFECT SENTENCE PARSING LATER ON. (NEEDED FOR NER and OPINIONATED CHECKS)

    # 4 LEMMATIZE!
    lemmatised_words = " ".join([t.lemma_ for t in doc])
    # print("After: ", lemmatised_words)
    return(lemmatised_words)

def pre_process(articles):
    for i in range(0, len(articles)):
        print("Number: ",   i)
        # print("HELLO: " ,articles[i])
        articles[i]["preprocessed_content"] =  basic_preprocess_keepstopwords(articles[i]["body"])
    return articles

# def basic_preprocess(self_text):
#      # 1. Remove html tags
#     words = BeautifulSoup(self_text).get_text()
#     # 2. Convert words to lower case and split each word up
#     words = self_text.lower()
#     # 3. Remove non-letters aka punctuation
#     words = re.sub("[^a-zA-Z]", " ", words).split()    
#     # 4 Remove stopwords
#     words = [word for word in words if word not in stops]
#     # 5 LEMMATIZE!
#     words = [lemmatizer.lemmatize(w) for w in words]
#         # 7. Join words back into one string, with a space in between each word
#     return(" ".join(words))

@app.route("/get_articles/<source>", methods=["GET"])
async def get_articles(source):
    articles = []
    print(source)
    if source == "All Sources":
        news_sources = ["atlantic", "bbc", "cnn", "dailymail",  "fox", "guardian", "independent", "nytimes", "skyau", "washington post"]
        for source in news_sources:
             with jsonlines.open(f'src/assets/articles_db/{source.lower()}.json', 'r') as jsonl_f:
                for line in jsonl_f:
                    articles.append(line)

    else:
        with jsonlines.open(f'src/assets/articles_db/{source.lower()}.json', 'r') as jsonl_f:
                for line in jsonl_f:
                    articles.append(line)
    # if source == "CNN":
    #     with jsonlines.open(f'src/assets/articles_db/cnn.jsonlines', 'r') as jsonl_f:
    #         for line in jsonl_f:
    #             articles.append(line)
            
    # elif source == "BBC":
    #     with jsonlines.open('src/assets/articles_db/bbc.json', 'r') as jsonl_f:
    #         for line in jsonl_f:
    #             articles.append(line)
    
    # processed_articles = pre_process(articles)
    processed_articles = articles
    if len(processed_articles) > 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "articles": processed_articles
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "No results found!"
            }
        ), 404


nerpipe = spacy.load(r"src/assets/NER model/model-best")
@app.route("/ner", methods=["POST"])
def ner():
    nerdict = {'PERSON': {}, 'ORG': {}, 'EVENT': {},
               'DATE': {}, 'GPE': {}, 'LOC': {}}
    nerdict = {'PERSON': {}, 'ORG': {}, 'EVENT': {}, 'GPE': {}, 'LOC': {}}
    if request.is_json:
        data = request.get_json()
        # print(data)
        content = data["body"]
        # Not that good after this
        # content = lemmatize_ner(content)
        # print(content)
        doc=nlp(content)
        for ent in doc.ents:
            if ent.label_ in nerdict.keys():
                clean_text = re.sub(r'[^\w\s]', '', ent.text)
                if ent.text in nerdict[ent.label_].keys():
                    nerdict[ent.label_][clean_text] += 1
                else:
                    nerdict[ent.label_][clean_text] = 1

        climatedoc = nerpipe(content)
        climatedict={}
        for ent in climatedoc.ents:
            # print(ent.label_)
            clean_text = re.sub(r'[^\w\s]', '', ent.text)
            if ent.text in climatedict.keys() and ent.label_ == "CLIMATE":
                climatedict[clean_text] += 1
            else:
                climatedict[clean_text] = 1
        nerdict["CLIMATE"] = climatedict
        for key in nerdict.keys():
            ndict = nerdict[key]
            keys = list(ndict.keys())
            values = list(ndict.values())
            sorted_value_index = np.argsort(values)[::-1]
            ndict = {keys[i]: values[i] for i in sorted_value_index}
            # ndict = [keys[i] for i in sorted_value_index]
            nerdict[key] = ndict

        return jsonify(
            {
                "code": 200,
                "data": {
                    "enitity": nerdict
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "Unable to get enitites"
            }
        ), 404

# -------------------------- CODE FOR SENTIMENT ANALYSIS --------------------------
def basic_sentiment_preprocess_keepstopwords(self_text):
    # 1. Remove html tags
    words = BeautifulSoup(self_text, features="html.parser").get_text()
    
    # 2. Convert words to lower case and split each word up
    words = words.lower()
    words = words.replace('\n','')

    # remove punctuation 
    punc = '''()-[]{};:\,<>/@#$%^&*_~'''
    for ele in punc:
        words = words.replace(ele, "")
    
    words = words.encode('ascii', 'ignore')
    words = words.decode()
    return words


def sentiment_analysis_vader(df):
    nerdict = ['PERSON', 'ORG', 'EVENT', 'GPE', 'LOC', 'CLIMATE']
    sid = SentimentIntensityAnalyzer()
    for ner in nerdict:
        sentiment_result_dict = {}
        for ner_term in df[ner]:
            result = sid.polarity_scores(df[ner][ner_term])

            if result['compound'] > 0.05:
                sentiment_result_dict[ner_term] =  ('Positive', result['compound'])
            elif result['compound'] < -0.05:
                sentiment_result_dict[ner_term] = ('Negative', result['compound'])
            else:
                sentiment_result_dict[ner_term] = ("Neutral", result['compound'])
                
            # print(sentiment_result_dict)
        df[ner] = sentiment_result_dict

    # print(df)  
    return df

fact_opinion_classifier = pipeline(model="lighteternal/fact-or-opinion-xlmr-el")
@app.route("/sentiment", methods=["POST"])
async def entity_level_sentiment_analysis():
    if request.is_json:
        data = request.get_json()
        content = data["body"]

        ner = requests.post("http://localhost:5001/ner", json={"body": content})
        ner = ner.json()
        ner = ner['data']['enitity']
        ner_dict = {}

        # split into sentence
        content = basic_sentiment_preprocess_keepstopwords(content)
        sentence_content = sent_tokenize(content)

        nerdict = {'PERSON': {}, 'ORG': {}, 'EVENT': {}, 'GPE': {}, 'LOC': {}, 'CLIMATE':{}}
        for entity in nerdict:
            ner_term_dict = {}
            for term in ner[entity]:
                term = term.replace("'", "")
                for idx, sentence in enumerate(sentence_content):
                    if term.lower() in sentence:
                        sentence_result = fact_opinion_classifier(sentence)[0]
                        
                        if sentence_result["label"] == "LABEL_0":
                            passage = ""
                            # get all the window sentences
                            if (len(sentence_content) == 1):
                                passage = sentence_content[0]
                            elif (idx != 0 and (idx != len(sentence_content) - 1)):
                                passage = sentence_content[idx-1] + sentence + sentence_content[idx+1]
                            # if it is the first sentence
                            elif (idx == 0):
                                passage = sentence + sentence_content[idx+1]
                            # if it is the last sentence
                            else:
                                passage = sentence_content[idx-1] + sentence 
                            
                            # add the sub-document
                            if term in ner_term_dict:
                                ner_term_dict[term] = ner_term_dict[term] + " " + passage
                            else:
                                ner_term_dict[term] = passage
                            
            ner_dict[entity] = ner_term_dict  

        ner_dict_final = sentiment_analysis_vader(ner_dict)

        for ner_entity in nerdict:
            for term in ner[ner_entity]:
                if (term in ner_dict_final[ner_entity]):
                    label, sentiment_score = ner_dict_final[ner_entity][term]
                else:
                    label, sentiment_score = ("Neutral", 0)
                nerdict[ner_entity][term] = (label, sentiment_score, ner[ner_entity][term])

        return jsonify(
            {
                "code": 200,
                "data": {
                    "entity_sentiment": nerdict
                }
            }
        )
    else:
        return jsonify(
            {
                "code": 404,
                "results": "Unable to get enitites"
            }
        ), 404


fact_opinion_classifier = pipeline(model="lighteternal/fact-or-opinion-xlmr-el")
# text="""The United States was established in 1776."""
# print("TESTINGGGGGGGGGG 1",fact_opinion_classifier(text))
text="""Fires and floods prove world leaders must act now on climate change"""
# print("TESTINGGGGGGGGGG 2",fact_opinion_classifier(text))
@app.route("/fact_opinion_classifier", methods=["POST"])
async def fact_opinion_classification():
    factual = None
    if request.is_json:
        data = request.get_json()
        content = data["body"]

        # IF ARTICLE LENGTH > 500, need to split it up
        # print("LENGTH BIG:" , len(content.split(" ")))
        if (len(content.split(" ")) > 200):
            content_splits = []
            # WISH TO KEEP THEIR SENTENCE STRUCTURES INTACT
            # SO SPLIT BY ". " first to get all sentences.
            content_sentences = content.split(". ")
            
            counter = 0
            temp_content_splits = ""
            for sen in content_sentences:
                if counter<200:
                    temp_content_splits += sen + ". "
                    counter += len(sen.split(" "))
                    # print("temp_content_splits: ",temp_content_splits)
                    
                else:
                    # Overflows reset counnter to 0
                    content_splits.append(temp_content_splits)
                    counter = 0
                    temp_content_splits = ""
            # print("HERE: ",content_splits)
            for split in content_splits:
                avg_score = 0
                # print("SPLIT: ", split)
                temp_classifier_results = fact_opinion_classifier(split)[0]
                # print("TESTING fact_opinion_classifier SPLITSSSS:--- ", fact_opinion_classifier(split))
                # IF FACTUAL, POSITIVE so we add
                if  temp_classifier_results["label"] == "LABEL_1":
                    avg_score += temp_classifier_results["score"]
                # ELSE IF OPINIONATED, NEGATIVE so we minus
                elif temp_classifier_results["label"] == "LABEL_0":
                    avg_score -= temp_classifier_results["score"]
            # IF avg_score POSITIVE, it means overall entire content is FACTUAL
            if avg_score >= 0:
                factual = True
            else:
                factual = False
        
        # NO NEED TO SPLIT, JUST RUN CLASSIFIER
        else:
            temp_classifier_results = fact_opinion_classifier(content)[0]
            #    print("TESTING fact_opinion_classifier:--- ", fact_opinion_classifier(content))
            if  temp_classifier_results["label"] == "LABEL_1":
                factual = True
            # ELSE IF OPINIONATED, NEGATIVE so we minus
            elif temp_classifier_results["label"] == "LABEL_0":
                factual = False

    if factual != None:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "result": factual
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "result": "Factual / Opinionated Classification FAILED!"
            }
        ), 404
    
# -------------------------- CODE FOR TEXT SUMMARISATION --------------------------
# Lexical Chain
def noun_relations(nouns):
    relation_list = defaultdict(list)
    for i in range(len(nouns)):
        relation = []
        for syn in wordnet.synsets(nouns[i], pos = wordnet.NOUN):
            for a in syn.lemmas():
                relation.append(a.name())
                if a.antonyms():
                    relation.append(a.antonyms()[0].name())
            for b in syn.hyponyms():
                if b.hyponyms():
                    relation.append(b.hyponyms()[0].name().split('.')[0])
            for c in syn.hypernyms():
                if c.hypernyms():
                    relation.append(c.hypernyms()[0].name().split('.')[0])
        relation_list[nouns[i]].append(relation)
    return relation_list

def generate_lexical_chain(nouns, relation_list):
    lexical = []
    threshold = 0.5
    for noun in nouns:
        flag = 0
        for j in range(len(lexical)):
            if flag == 0:
                for key in list(lexical[j]):
                    if key == noun and flag == 0:
                        lexical[j][noun] +=1
                        flag = 1
                    elif key in relation_list[noun][0] and flag == 0:
                        syns1 = wordnet.synsets(key, pos = wordnet.NOUN)
                        syns2 = wordnet.synsets(noun, pos = wordnet.NOUN)
                        if syns1[0].wup_similarity(syns2[0]) >= threshold:
                            lexical[j][noun] = 1
                            flag = 1
                    elif noun in relation_list[key][0] and flag == 0:
                        syns1 = wordnet.synsets(key, pos = wordnet.NOUN)
                        syns2 = wordnet.synsets(noun, pos = wordnet.NOUN)
                        if syns1[0].wup_similarity(syns2[0]) >= threshold:
                            lexical[j][noun] = 1
                            flag = 1
        if flag == 0: 
            new_dict = {}
            new_dict[noun] = 1
            lexical.append(new_dict)
            flag = 1
    return lexical

def prune(lexical):
    final_chain = []
    while lexical:
        result = lexical.pop()
        if len(result.keys()) == 1:
            for value in result.values():
                if value != 1: 
                    final_chain.append(result)
        else:
            final_chain.append(result)
    return final_chain

threshold_min = 0.1
threshold_max = 0.9

def return_frequencies(words, lexical_chain):
    frequencies = defaultdict(int)
    for word in words:
        for w in word:
            if w not in STOPS:
                flag = 0
                for i in lexical_chain:
                    if w in list(i.keys()):
                        frequencies[w] = sum(list(i.values()))
                        flag = 1
                        break
                if flag == 0: 
                    frequencies[w] += 1
    m = float(max(frequencies.values()))
    for w in list(frequencies.keys()):
        frequencies[w] = frequencies[w]/m
        if frequencies[w] >= threshold_max or frequencies[w] <= threshold_min:
            del frequencies[w]
    return frequencies

def summarize(sentence, lexical_chain, n):
    assert n <= len(sentence)
    word_sentence = [word_tokenize(s.lower()) for s in sentence]
    frequencies = return_frequencies(word_sentence, lexical_chain)
    ranking = defaultdict(int)
    for i, sent in enumerate(word_sentence):
        for word in sent:
            if word in frequencies:
                ranking[i] += frequencies[word]
                idx = rank(ranking, n)
    final_index = sorted(idx)
    return [sentence[j] for j in final_index]

def rank(ranking, n):
    return nlargest(n, ranking, key=ranking.get)

position = ['NN', 'NNS', 'NNP', 'NNPS']
tokenizer = RegexpTokenizer(r'\w+')


def generate_lexical_chain_summary(input_content):
    sentence = sent_tokenize(input_content)
    tokens = [tokenizer.tokenize(w) for w in sentence]
    tagged =[pos_tag(tok) for tok in tokens]
    nouns = [word.lower() for i in range(len(tagged)) for word, pos in tagged[i] if pos in position]
    relation = noun_relations(nouns)
    lexical = generate_lexical_chain(nouns, relation)
    final_chain = prune(lexical)
    if len(sentence) >= 3:
        n = 3
    else: 
        n = 1
    s = summarize(sentence, final_chain, n)
    return [final_chain, s]

# TF-IDF
def basic_preprocess(self_text):
     # 1. Remove html tags
    words = BeautifulSoup(self_text).get_text()
    # 2. Convert words to lower case and split each word up
    words = self_text.lower()
    # 3. Remove non-letters aka punctuation
    words = re.sub("[^a-zA-Z]", " ", words).split()    
    # 4 Remove stopwords
    words = [word for word in words if word not in STOPS]
    # 5 LEMMATIZE!
    words = [lemmatizer.lemmatize(w) for w in words]
    # 7. Join words back into one string, with a space in between each word
    return(" ".join(words))

def top_sentence(input_doc, limit):
    keyword = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    doc = nlp(input_doc)
    processed_doc = nlp(basic_preprocess(input_doc))
    for token in processed_doc:
        if token.pos_ in pos_tag:
            keyword.append(token.text)
    freq_word = Counter(keyword)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for w in freq_word:
        freq_word[w] = freq_word[w] / max_freq
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]
    summary = []
    sorted_x = sorted(sent_strength.items(), key = lambda kv: kv[1], reverse = True)
    counter = 0
    for i in range(len(sorted_x)):
        summary.append(str(sorted_x[i][0]).capitalize())
        counter += 1
        if(counter >= limit):
            break
    return ' '.join(summary)

# Abstractive Summarisation
model_name = 'google/pegasus-xsum'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

@app.route("/summarisation", methods=["POST"])
def summarisation():
    if request.is_json:
        data = request.get_json()
        content = data["body"]
        content = content.replace("\n", "")
        content = content.replace("  ", "")
        content = content.replace("\'", "'")
        chains = generate_lexical_chain_summary(content)[0]
        lc_summary = " ".join(generate_lexical_chain_summary(content)[1])
        tf_idf_summary = top_sentence(content, 3)
        tr_summary = []
        for sent in nlp(content)._.textrank.summary(limit_phrases = 15, limit_sentences = 3):
            tr_summary.append(str(sent))
        new_tr_summary = " ".join(tr_summary)
        batch = tokenizer.prepare_seq2seq_batch(content, truncation = True, padding = 'longest', return_tensors ='pt')
        translated = model.generate(**batch)
        ab_summary = tokenizer.batch_decode(translated, skip_special_tokens = True)
        return jsonify(
            {
                "code": 200,
                "data": {
                    "lc_summary": lc_summary,
                    "chains": chains,
                    "tf_idf_summary": tf_idf_summary,
                    "tr_summary": new_tr_summary,
                    "ab_summary": ab_summary
                }
            }
        ), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "Unable to get summary"
            }
        ), 404
# -------------------------- CODE FOR TEXT SUMMARISATION - END --------------------------

# Pass document into LDA model and return dominant topic

lda_model=gensim.models.ldamodel.LdaModel.load("C:/Dev/News-Summariser_new/src/flask/climate_lda.gensim")
dictionary = lda_model.id2word

@app.route("/ldatopic", methods=["POST"])
def retrieve_dominant_topic():
    topics = {0: "Environmental Impact", 1: "Social Impact", 2: "Environmental Politics", 3:"Economic Impact"}
    if request.is_json:
        data = request.get_json()
        content = data["body"]
        content = content.replace("\n", "")
        content = content.replace("  ", "")
        content = content.replace("\'", "'")
        content_bow = dictionary.doc2bow(content.lower().split())
        document_topics = lda_model.get_document_topics(content_bow)
        dominant_topic = max(document_topics, key=lambda item: item[1])[0]
        # print("document_topics: ",document_topics)
        # document_topics:  [(0, 0.7444019), (3, 0.25354826)]
        resulting_topics = []
        for topic_tuple in document_topics:
            temp_score = round(float(topic_tuple[1]) * 100 ,2)
            resulting_topics.append({"topic": topics[topic_tuple[0]], "score":temp_score })
        print("resulting_topics: ",resulting_topics)
        return jsonify(
            {
                "code": 200,
                "data": {
                    "dominant_topic": topics[dominant_topic],
                    "topics_overall" : resulting_topics 
                }
            }
        ), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "Unable to get dominant topic"
            }
        ), 404
    
# code for retrieving most dominant topic
if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": News Feed")
    app.run(host='0.0.0.0', port=5001, debug=True)
