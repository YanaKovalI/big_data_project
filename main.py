import requests
import pandas as pd
import extract_entities
import json
import re
import nltk.stem.porter 


url = "https://www.wikidata.org/w/api.php"

input_table = pd.read_csv("countries_database.csv")

entities = extract_entities.extract_entities_from_table(input_table)
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

# print(information)
# print("\n\n")

#compute weights for labels
entity_vector = {}
for entity,labels in information.items():
    new_entity = entity.replace(" ", "")
    vector = {}
    for label in labels:
        new_label =  re.sub(r'[^a-zA-Z0-9]', '', label)
        #stemmer to extract stems of the words
        porter_stemmer = nltk.PorterStemmer()
        if (new_entity.lower() in new_label.lower()) | (porter_stemmer.stem(new_entity) in new_label.lower()):
            if len(new_entity) == len(new_label):
                weight = 1
            elif len(new_entity) < len(new_label):
                weight = (1 - 2/(len(new_label) - len(new_entity))) + 0.000001
        else:
            weight = 0
        vector[label] = weight
    entity_vector[entity] = vector

print(entity_vector)
