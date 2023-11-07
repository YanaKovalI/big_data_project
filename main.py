import requests
import pandas as pd
import extract_entities
import json

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
for result in results:
    print(f"NEW ENTITY {result}\n\n\n")
    

information = {}  # Initialize the information dictionary "entity" : [list of labels]

for entity, result in zip(entities, results):
    labels = []  # Initialize a list to store labels for each entity
    for item in result.get("search", []):
        label = item.get("display", {}).get("label", {}).get("value")
        labels.append(label)

    # Store the labels list for the current entity
    information[entity] = labels

print(information)




# print(information)        