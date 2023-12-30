import json
from SPARQLWrapper import SPARQLWrapper, JSON
import labelsdb_wiki
import requests
import pandas as pd
import extract_entities
import json
import re
import label_search_wikidata

cache = dict()


def get_weighted_labels(entities):
    entities_weighted_labels = dict()
    entity_labels = dict()
    for entity in entities:
        try:
            weighted_labels = labelsdb_wiki.get_weighted_labels(entity)
            if weighted_labels is not None:
                entities_weighted_labels[entity] = weighted_labels
                print("Calculated {0} weighted labels for entity {1} ({2})".format(len(weighted_labels), entity, len(entities)))
            else:
                entity_labels[entity] = get_labels_by_query(entity)

        except Exception as e:
            entity_labels[entity] = get_labels_by_query(entity)

    entities_not_in_db = list(entity_labels.keys())
    for entity in entities_not_in_db:
        labels = entity_labels[entity]

        if labels:
            weighted_labels = get_weights(labels)
            labelsdb_wiki.put_weighted_labels(entity, weighted_labels)
        else:
            weighted_labels = dict()
            labelsdb_wiki.put_labelless_entity(entity)

        entities_weighted_labels[entity] = weighted_labels
        print("Calculated {0} weighted labels for entity {1} ({2}})".format(len(weighted_labels), entity, len(entities)))
    return entities_weighted_labels

def get_weights(labels):
    weighted_labels = dict()
    for label in labels:
        try:
            weight = labelsdb_wiki.get_weight(label)
            if weight:
                weighted_labels[label] = weight
        except Exception as e:
            print(e)
    labels2 = list(set(labels) - set(weighted_labels.keys()))
    if labels:
        weighted_labels_chunked = get_weighted_labels_in_chunks(labels2)
        if weighted_labels_chunked:
            weighted_labels = weighted_labels | weighted_labels_chunked
        else:
            for label in labels2:
                weighted_labels[label] = get_weights_for_single_label(label)
    return weighted_labels

def get_weighted_labels_in_chunks(labels):
    if not labels:
        return dict()
    try:
        entity_labels_chunks = list()
        for i in range(0, len(labels), 100):
            entity_labels_chunks.append(labels[i:i + 100])
        weighted_labels = dict()
        for chunk in entity_labels_chunks:
            weighted_labels = weighted_labels | get_weights_with_one_query(chunk)
        return weighted_labels
    except Exception as e:
        print(e)
        tuples = [(l, 0) for l in labels]
        return dict(tuples)
    
    
def get_labels_by_query(entity):
    entity = entity.replace(" ", "_")
    url = "https://www.wikidata.org/w/api.php"

    results = []

    
    params = {
        "action" : "wbsearchentities",
        "language" : "en",
        "format" : "json",
        "search" : entity
    }
    data =  requests.get(url, params = params)
    results.append(data.json())
    
    labels = []  
    for item in results.get("search", []):
        label = item.get("display", {}).get("label", {}).get("value")
        if label not in labels:
                labels.append(label)
    return list(set(labels))

def get_weights_with_one_query(labels):
    label_weights = {}
    for label in labels:
        num_entities = label_search_wikidata.get_number_of_entities_for_label(label)
        if num_entities != 0:  # Check if the number of entities is not zero
            label_weights[label] = 1 / num_entities
        else:
            label_weights[label] = 0  
    return label_weights

def get_weights_for_single_label(label):
    label = label.replace(" ", "_")
    num_entities = label_search_wikidata.get_number_of_entities_for_label(label)
    if num_entities != 0:  # Check if the number of entities is not zero
        weight = 1 / num_entities
    else:
        weight = 0  
    return weight

