import csv
import json
import os
import pandas as pd


def find_labels(entity):
    entity = entity.lower()
    id = find_context_id(entity)
    context = find_context(id)
    labels = extract_nouns(context)
    weightedLabels = apply_weights(labels)
    return weightedLabels


def find_classes(entities):
    entities = [e.lower() for e in entities]
    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, 'dataset')
    classes = {}
    for e in entities:
        classes[str(e)] = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                print(str(file))
                filename = os.path.join(directory, file)
                tuple_table = pd.read_csv(filename)
                query_result = tuple_table[tuple_table['instance'].isin(entities)]
                print(query_result)
                # for row in tuple_table.iterrows():
                #     row = row[1]
                #     if row['instance'] in entities:
                #         classes[row['instance']].add(row['class'])
                #         print(classes)
    # print(classes)


def find_context_id(entity):
    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, 'dataset')
    file_set = set()
    count = 0
    classes = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            # if file.endswith(".csv"):
            if file.endswith("ihr.csv"):
                print(str(file))
                filename = os.path.join(directory, file)
                tuple_table = pd.read_csv(filename)
                for row in tuple_table.iterrows():
                    row = row[1]
                    if row['instance'] == entity:
                        file_set.add(file)
                        classes.add(row['class'])
                        count += 1
                        # modifications = row['modifications']
                        # json_mod = json.loads(modifications)[0]
                        # provids = json_mod['provids']
                        # print(provids)
    print("For the entity " + str(entity) + " were " + str(count) + " entries in " + str(
        len(file_set)) + " different files found.")
    print("The different classes are " + str(classes))


def find_context(id):
    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, 'dataset/context')
    print(directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(directory, file)
                context_table = pd.read_csv(filename)


def extract_nouns(context):
    nlp = spacy.load("en")
    doc = nlp(context)
    for np in doc.noun_chunks:
        print(np)
    return ""


def apply_weights(labels):
    weightedLabels = {}
    for label in labels:
        weightedLabels[label] = 1
    return weightedLabels


ents = ["Germany", "France", "Austria", "Japan"]

find_classes(ents)

# find_context_id("aang")
# find_context_id("time")
# find_labels("aang")
# find_labels("Germany")
