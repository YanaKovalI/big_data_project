import requests
import pandas as pd
import extract_entities
import json
import re
import label_search_wikidata

# input_table = pd.read_csv(csv_file_table)
# entities = extract_entities.extract_entities_from_table(input_table)

#as an input should be a csv_file, return a dictionary entities with lists of weights
def get_entity_info(entities):
    url = "https://www.wikidata.org/w/api.php"

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
 

    information = {}  # Initialize the information dictionary "entity" : [list of labels]

    for entity, result in zip(entities, results):
        labels = []  # Initialize a list to store labels for each entity
        for item in result.get("search", []):
            label = item.get("display", {}).get("label", {}).get("value")
            if label not in labels:
                labels.append(label)
        # Store the labels list for each entity
        information[entity] = labels
    return information