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

def get_weights(information):
    porter_stemmer = nltk.PorterStemmer()

    weighted_informations = {}

    for entity,labels in information.items():

        label_nouns = []

        for label in labels:

            label_tokens = label.split()
            tags = nltk.pos_tag(label_tokens)
            nouns = [word for word,pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]

            label_nouns.extend(nouns)

        noun_counter = dict(Counter(label_nouns))
        max_noun_appearence = max(noun_counter.values())

        weighted_informations[entity] = {}

        for noun,count in noun_counter.items():

            weighted_informations[entity][noun] = count/max_noun_appearence

    display(weighted_informations)

    return weighted_informations

get_weights(information)
