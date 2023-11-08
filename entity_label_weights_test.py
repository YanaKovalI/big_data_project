import requests
import pandas as pd
import json
import re
import nltk.stem.porter 


url = "https://www.wikidata.org/w/api.php"

input_table = pd.read_csv("countries_database.csv")

#entities = extract_entities.extract_entities_from_table(input_table)
entities = input_table.iloc[:, 0].tolist()
results = []

for entity in entities:
    params = {
    "action" : "wbsearchentities",
    "language" : "en",
    "format" : "json",
    "search" : entity
}
    data =  requests.get(url, params = params)
    results.append(data.json())


# just print  json results for each entity
# for result in results:
#     print(f"NEW ENTITY {result}\n\n\n")
#     print("\n\n")

information = {}  # Initialize the information dictionary "entity" : [list of labels]

for entity, result in zip(entities, results):
    labels = []  # Initialize a list to store labels for each entity
    for item in result.get("search", []):
        label = item.get("display", {}).get("label", {}).get("value")
        labels.append(label)

    # Store the labels list for each entity
    information[entity] = labels

############################################
#NEW PART
############################################
import nltk
#nltk.download('averaged_perceptron_tagger')
from collections import Counter
import math

porter_stemmer = nltk.PorterStemmer()

noun_informations = {}

#Get all nouns (and adjectives) from all labels of an entity and count their appearence

for entity,labels in information.items():

    label_nouns = []

    for label in labels:
        
        label_tokens = label.split()
        tags = nltk.pos_tag(label_tokens)
        nouns = [word for word,pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or pos == 'JJ')]

        label_nouns.extend(nouns)

    noun_informations[entity] = dict(Counter(label_nouns))

#calculate based on the appearence of each noun the label weight for each label of an entity

for entity,labels in information.items():

    noun_counter = noun_informations[entity]
    noun_list = list(noun_counter.keys())
    noun_total = sum(noun_counter.values())
    print(noun_counter)

    for label in labels:

        label_noun_appearence = 0

        for token in label.split():

            if token in noun_list:

                label_noun_appearence += noun_counter[token]

        print(label,label_noun_appearence, label_noun_appearence/(noun_total*len(label.split())))
