import requests
import pandas as pd
import extract_entities
import json
import re


#as an input should be a csv_file
def get_entity_info(csv_file_table):
    url = "https://www.wikidata.org/w/api.php"

    input_table = pd.read_csv(csv_file_table)

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
    return information


def get_weighted_labels(csv_file_table):
    information = get_entity_info(csv_file_table)
    # Compute weights for labels
    label_counts = {}  # Dictionary to store the count of occurrences for each label
    entity_occurrences = {}  # Dictionary to track if a label has occurred in an entity

    for labels_list in information.values():
        labels_set = set()  # Use a set to keep track of labels within an entity without duplication
        for label in labels_list:
            if label:
                # Remove special characters and convert to lowercase for better matching
                label_new = re.sub(r'[^a-zA-Z0-9\s]', '', label.lower())

                # Check if the label has not occurred in this entity before
                if label_new not in labels_set:
                    label_counts[label_new] = label_counts.get(label_new, 0) + 1
                    labels_set.add(label_new)

    # Calculate weights based on the inverse of label counts
    for entity, labels_list in information.items():
        labels_weights = {}  # Dictionary to store labels and their corresponding weights
        for label in labels_list:
            if label:
                label_key = re.sub(r'[^a-zA-Z0-9\s]', '', label.lower())
                weight = 1/ label_counts[label_key]
                labels_weights[label_key] = weight
        # Store the labels and weights for each entity
        information[entity] = labels_weights
    # Print the resulting information dictionary
    return json.dumps(information, indent=2)


def get_domain_size_labels(csv_file_table):
    information = get_entity_info(csv_file_table)
    label_counts = {}  # Dictionary to store the count of occurrences for each label
    entity_occurrences = {}  # Dictionary to track if a label has occurred in an entity
    #compute domain size for labels
    for labels_list in information.values():
        labels_set = set()  # Use a set to keep track of labels within an entity without duplication
        for label in labels_list:
            if label:
                # Remove special characters and convert to lowercase for better matching
                label_new = re.sub(r'[^a-zA-Z0-9\s]', '', label.lower())

                # Check if the label has not occurred in this entity before
                if label_new not in labels_set:
                    label_counts[label_new] = label_counts.get(label_new, 0) + 1
                    labels_set.add(label_new)

    # Calculate weights based on the inverse of label counts
    for entity, labels_list in information.items():
        labels_domains = {}  # Dictionary to store labels and their corresponding weights
        for label in labels_list:
            if label:
                label_key = re.sub(r'[^a-zA-Z0-9\s]', '', label.lower())
                domain = label_counts[label_key]
                labels_domains[label_key] = domain
        # Store the labels and weights for each entity
        information[entity] = labels_domains
    # Print the resulting information dictionary
    return json.dumps(information, indent=2)