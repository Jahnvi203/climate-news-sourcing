import matplotlib.pyplot as plt
from collections import Counter
import spacy
import pandas as pd
import numpy as np
import nltk
import jsonlines
import re
import os
import sys
import gensim
from nltk.corpus import stopwords
from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import ast
app = Flask(__name__)
CORS(app)

STOPS = set(stopwords.words('english'))
STOPS.add("CNN")
STOPS.add("cnn")
STOPS.add("bbc")
STOPS.add("BBC")

def preprocess(text):
    text = re.sub("[^a-zA-Z]", " ", text).split()
    meaningful_words = [w for w in text if w not in STOPS]
    return (" ".join(meaningful_words))


articles = []
climate = []
event = []
gpe = []
loc = []
person = []
org = []

nerpipe = spacy.load(f'src/assets/NER model/model-best')
nlp = spacy.load('en_core_web_sm')
def generatedata():
    with jsonlines.open(f'src/assets/articles_db/cnn.json', 'r') as jsonl_f:
        for line in jsonl_f:
            articles.append(line)

    with jsonlines.open(f'src/assets/articles_db/bbc.json', 'r') as jsonl_f:
        for line in jsonl_f:
            articles.append(line)

    for article in articles:
        # if "headline" in article.keys():
        #     text = preprocess(article.get('headline'))
        text = preprocess(article.get('body'))
        doc = nlp(text)
        print("running")
        for ent in doc.ents:
            clean_text = re.sub(r'[^\w\s]', '', ent.text)
            if ent.label_ == "EVENT":
                event.append(clean_text)
            elif ent.label_ == "GPE":
                gpe.append(clean_text)
            elif ent.label_ == "LOC":
                loc.append(clean_text)
            elif ent.label_ == "PERSON":
                person.append(clean_text)
            elif ent.label_ == "ORG":
                org.append(clean_text)

        climatedoc = nerpipe(text)
        print("running climate")
        for ent in climatedoc.ents:
            clean_text = re.sub(r'[^\w\s]', '', ent.text)
            if ent.label_ == "CLIMATE":
                climate.append(clean_text)

    with open('src/assets/NER model/climate.txt', 'w') as f:
        for line in climate:
            f.write(f"{line}\n")
    with open('src/assets/NER model/event.txt', 'w') as f:
        for line in event:
            f.write(f"{line}\n")
    with open('src/assets/NER model/gpe.txt', 'w') as f:
        for line in gpe:
            f.write(f"{line}\n")
    with open('src/assets/NER model/loc.txt', 'w') as f:
        for line in loc:
            f.write(f"{line}\n")
    with open('src/assets/NER model/org.txt', 'w') as f:
        for line in org:
            f.write(f"{line}\n")
    with open('src/assets/NER model/person.txt', 'w') as f:
        for line in person:
            f.write(f"{line}\n")

# generatedata()

@app.route("/perbar")
def person_barchart():
    person = []
    with open('src/assets/NER model/person.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            person.append(line)
    if person !=[]:
        enitity, values = zip(*(Counter(person).most_common(20)))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "entity": enitity,
                    "values": values,
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "No results found!"
            }
        ), 404
    # plt.bar(enitity, values)
    # plt.xticks(fontsize=7.5, rotation=45)
    # plt.show()


@app.route("/orgbar")
def org_barchart():
    org = []
    with open('src/assets/NER model/org.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            org.append(line)
    if org != []:
        enitity, values = zip(*(Counter(org).most_common(20)))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "entity": enitity,
                    "values": values,
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "No results found!"
            }
        ), 404
    


@app.route("/gpebar")
def gpe_barchart():
    gpe = []
    with open('src/assets/NER model/gpe.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            gpe.append(line)
    if gpe != []:
        enitity, values = zip(*(Counter(gpe).most_common(20)))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "entity": enitity,
                    "values": values,
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "No results found!"
            }
        ), 404


@app.route("/locbar")
def loc_barchart():
    loc = []
    with open('src/assets/NER model/loc.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            loc.append(line)
    if loc != []:
        enitity, values = zip(*(Counter(loc).most_common(20)))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "entity": enitity,
                    "values": values,
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "No results found!"
            }
        ), 404
        

@app.route("/sentiment")
def sentiment():
    
    with open('src/assets/sentiment/person_ner_sentiment.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            person = ast.literal_eval(line)
    with open('src/assets/NER model/person_response.txt', 'r') as f:
        person_freq=""
        for line in f:
            line = line.rstrip('\n')
            line = line.strip()
            person_freq+=line
        person_freq=person_freq.split("]")
        person_freq = person_freq[-2].split(":")
        person_freq = person_freq[-1]+"]"
        value = ast.literal_eval(person_freq)
        # print(value,type(value))
        for i in range(len(value)):
            keys = list(person.keys())
            person[keys[i]] = person[keys[i]],value[i]
    # print(person)


    with open('src/assets/sentiment/org_ner_sentiment.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            org = ast.literal_eval(line)
            # print(org)
    with open('src/assets/NER model/org_response.txt', 'r') as f:
        org_freq=""
        for line in f:
            line = line.rstrip('\n')
            line = line.strip()
            org_freq += line
        org_freq = org_freq.split("]")
        org_freq = org_freq[-2].split(":")
        org_freq = org_freq[-1]+"]"
        value = ast.literal_eval(org_freq)
        # print(value,type(value))
        for i in range(len(value)):
            keys = list(org.keys())
            org[keys[i]] = org[keys[i]], value[i]
    # print(org)


    with open('src/assets/sentiment/gpe_ner_sentiment.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            gpe = ast.literal_eval(line)
    with open('src/assets/NER model/gpe_response.txt', 'r') as f:
        gpe_freq = ""
        for line in f:
            line = line.rstrip('\n')
            line = line.strip()
            gpe_freq += line
        gpe_freq = gpe_freq.split("]")
        gpe_freq = gpe_freq[-2].split(":")
        gpe_freq = gpe_freq[-1]+"]"
        value = ast.literal_eval(gpe_freq)
        # print(value,type(value))
        for i in range(len(value)):
            keys = list(gpe.keys())
            gpe[keys[i]] = gpe[keys[i]], value[i]
    # print(gpe)

    with open('src/assets/sentiment/loc_ner_sentiment.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            loc = ast.literal_eval(line)
    with open('src/assets/NER model/loc_response.txt', 'r') as f:
        loc_freq = ""
        for line in f:
            line = line.rstrip('\n')
            line = line.strip()
            loc_freq += line
        loc_freq = loc_freq.split("]")
        loc_freq = loc_freq[-2].split(":")
        loc_freq = loc_freq[-1]+"]"
        value = ast.literal_eval(loc_freq)
        # print(value,type(value))
        for i in range(len(value)):
            keys = list(loc.keys())
            loc[keys[i]] = loc[keys[i]], value[i]
    # print(loc)

    with open('src/assets/sentiment/event_ner_sentiment.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            event = ast.literal_eval(line)
    with open('src/assets/NER model/event_response.txt', 'r') as f:
        event_freq = ""
        for line in f:
            line = line.rstrip('\n')
            line = line.strip()
            event_freq += line
        event_freq = event_freq.split("]")
        event_freq = event_freq[-2].split(":")
        event_freq = event_freq[-1]+"]"
        # print(event_freq)
        value = ast.literal_eval(event_freq)
        # print(value,type(value))
        for i in range(len(value)):
            keys = list(event.keys())
            event[keys[i]] = event[keys[i]], value[i]
    # print(event)

    with open('src/assets/sentiment/climate_ner_sentiment.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            climate = ast.literal_eval(line)
    with open('src/assets/NER model/climate_response.txt', 'r') as f:
        climate_freq = ""
        for line in f:
            line = line.rstrip('\n')
            line = line.strip()
            climate_freq += line
        climate_freq = climate_freq.split("]")
        climate_freq = climate_freq[-2].split(":")
        climate_freq = climate_freq[-1]+"]"
        # print(event_freq)
        value = ast.literal_eval(climate_freq)
        # print(value,type(value))
        for i in range(len(value)):
            keys = list(climate.keys())
            climate[keys[i]] = climate[keys[i]], value[i]
    # print(climate)


    return jsonify(
        {
            "code": 200,
            "data": {
                "org": org,
                "person": person,
                "gpe":gpe,
                "loc":loc,
                "event":event,
                "climate":climate
            }
        }), 200



            
    # print(person,type(person))
    
    


@app.route("/eventbar")
def event_barchart():
    event = []
    with open('src/assets/NER model/event.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            event.append(line)
    if event !=[]:
        enitity, values = zip(*(Counter(event).most_common(20)))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "entity": enitity,
                    "values": values,
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "No results found!"
            }
        ), 404
    
    

@app.route("/climatebar")
def climate_barchart():
    climate = []
    with open('src/assets/NER model/climate.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            climate.append(line)
    if climate !=[]:
        enitity, values = zip(*(Counter(climate).most_common(20)))
        return jsonify(
            {
                "code": 200,
                "data": {
                    "entity": enitity,
                    "values": values,
                }
            }), 200
    else:
        return jsonify(
            {
                "code": 404,
                "results": "No results found!"
            }
        ), 404
    
lda_model=gensim.models.ldamodel.LdaModel.load("src/flask/climate_lda.gensim")
dictionary = lda_model.id2word

def lda():
    with jsonlines.open(f'src/assets/articles_db/cnn.json', 'r') as jsonl_f:
        for line in jsonl_f:
            articles.append(line)
    topicarticles={0:[],1:[],2:[],3:[]}
    print("loading")
    for article in articles:
        # if "headline" in article.keys():
        #     text = preprocess(article.get('headline'))
        
        topics = {0: "Environmental Impact", 1: "Social Impact", 2: "Environmental Politics", 3:"Economic Impact"}
        content = preprocess(article.get('body'))
        content = content.replace("\n", "")
        content = content.replace("  ", "")
        content = content.replace("\'", "'")
        content_bow = dictionary.doc2bow(content.lower().split())
        document_topics = lda_model.get_document_topics(content_bow)
        dominant_topic = max(document_topics, key=lambda item: item[1])[0]
        print(dominant_topic)
        topicarticles[dominant_topic].append(content)
        # topicarticles[dominant_topic] = topicarticles[dominant_topic]+content
        # print("document_topics: ",document_topics)
    # print(topicarticles)
    with open('src/assets/lda_model/topic.txt', 'w') as f:
        f.write(str(topicarticles))
# lda()
def ldata():
    with open('src/assets/lda_model/topic.txt', 'r') as f:
        topic_dict = ""
        for line in f:
            line = line.rstrip('\n')
            line = line.strip()
            topic_dict += line
            value = ast.literal_eval(topic_dict)
            print(value,type(value))
        keys = list(value.keys())
        for key in keys:
            articles_in_topic = value[key]
            climate = []
            event = []
            gpe = []
            loc = []
            person = []
            org = []
            topic={"climate":[],"event":[],"gpe":[],"loc":[],"person":[],"org":[]}
            for article in articles_in_topic:
                doc = nlp(article)
                climatedoc = nerpipe(article)
                for ent in doc.ents:
                    clean_text = re.sub(r'[^\w\s]', '', ent.text)
                    if ent.label_ == "EVENT":
                        event.append(clean_text)
                    elif ent.label_ == "GPE":
                        gpe.append(clean_text)
                    elif ent.label_ == "LOC":
                        loc.append(clean_text)
                    elif ent.label_ == "PERSON":
                        person.append(clean_text)
                    elif ent.label_ == "ORG":
                        org.append(clean_text)
                for ent in climatedoc.ents:
                    clean_text = re.sub(r'[^\w\s]', '', ent.text)
                    if ent.label_ == "CLIMATE":
                        climate.append(clean_text)
            topic['climate'] = Counter(climate).most_common(10)
            topic['event'] = Counter(event).most_common(10)
            topic['gpe'] = Counter(gpe).most_common(10)
            topic['loc'] = Counter(loc).most_common(10)
            topic['person'] = Counter(person).most_common(10)
            topic['org'] = Counter(org).most_common(10)
            value[key] = topic
    with open('src/assets/lda_model/topic_entity.txt', 'w') as f:
        f.write(str(value))
                
# ldata()


@app.route("/lda")
def lchart():
    with open('src/assets/lda_model/topic_entity.txt', 'r') as f:
        topic_dict = ""
        for line in f:
            line = line.rstrip('\n')
            line = line.strip()
            topic_dict += line
        value = ast.literal_eval(topic_dict)
        # print(value[2], type(value))
    with app.app_context():
        if value :
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "lda": value,
                
                    }
                }), 200
        else:
            return jsonify(
                {
                    "code": 404,
                    "results": "No results found!"
                }
            ), 404


lchart()
if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": Ner")
    app.run(host='0.0.0.0', port=5002, debug=True)
