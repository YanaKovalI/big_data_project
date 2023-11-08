import csv
import os
import pandas as pd
import spacy
    
def findLabels(entity):
    id = findContextID(entity)
    context = findContext(id)
    labels = extractNouns(context)
    weightedLabels = applyWeights(labels)
    return weightedLabels
    
def findContextID(entity):
    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, 'dataset')
    print(directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(directory, file)
                tuple_table = pd.read_csv(filename)
                if (tuple_table[2] == entity):
                    return tuple_table[id]
                
def findContext(id):
    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, 'dataset/context')
    print(directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(directory, file)
                context_table = pd.read_csv(filename)

def extractNouns(context):
    nlp = spacy.load("en")
    doc = nlp(context)
    for np in doc.noun_chunks:
        print(np)
    return ""

def applyWeights(labels):
    weightedLabels = {}
    for label in labels:
        weightedLabels[label] = 1
    return weightedLabels

findLabels("Germany")