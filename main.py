import os
import time

import dbpedia
import extract_entities
import get_info_from_wikidata
import datetime

import labelsdb
import query_webisa
import relatedness
import label_search_wikidata
from label_search_wikidata import SPARQLQueryDispatcher
import json
import pandas as pd
import labelsdb_wiki
         
def get_relatedness_for_multiple_tables_dbpedia(table1="data/example_dataset/countries8.csv", order_path = 'data\\example_dataset', n1=1.0, n2=1.0, m1=1.0, m2=1.0):
    labelsdb.init_database()

    query_time = 0
    calculation_time = 0

    entities1 = extract_entities.extract_entities_from_table(table1)
    dbpedia_labels1 = dbpedia.get_weighted_labels(entities1)
    table_relatedness = dict()

    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, order_path)
    for root, dirs, files in os.walk(directory):
        file_number = 1
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(order_path, file)

                start = time.time()

                entities2 = extract_entities.extract_entities_from_table(filename)
                dbpedia_labels2 = dbpedia.get_weighted_labels(entities2)

                query_stop = time.time()
                query_time += query_stop - start

                r3 = relatedness.get_set_relatedness_expansion(dbpedia_labels1, dbpedia_labels2, n1, n2, m1, m2)
                table_relatedness[file] = r3

                calculation_stop = time.time()
                calculation_time += calculation_stop - query_stop
                print("\nCalculated relatedness for file {0} ({1}/{2})\n".format(str(file), str(file_number), len(files)))
                file_number += 1

    sorting_stop = time.time()

    sorted_relatedness = dict(sorted(table_relatedness.items(), key=lambda item: item[1], reverse=True))

    calculation_time += time.time() - sorting_stop

    print("\n")
    print("RESULT after {0} of getting labels and {1} of calculating:".format(query_time, calculation_time))
    print("Relatedness between {0} and all tables is: {1}".format(str(table1), sorted_relatedness))
    print("Top 5 related tables are:")
    i = 0
    for key, value in sorted_relatedness.items():
        if i >= 5:
            break
        i += 1
        print("{0}: {1}".format(key, value))


def get_relatedness_for_multiple_tables_wiki(table1="data/example_dataset/countries8.csv", order_path = 'data\\example_dataset', n1=1.0, n2=1.0, m1=1.0, m2=1.0):
    labelsdb_wiki.init_database()
    query_time = 0
    calculation_time = 0

    entities1 = extract_entities.extract_entities_from_table(table1)
    wikidata_labels1 = get_info_from_wikidata.get_entity_info(entities1)
    wikidata_weighted_labels1 = label_search_wikidata.get_weighted_labels(wikidata_labels1)
    table_relatedness = dict()

    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, order_path)
    for root, dirs, files in os.walk(directory):
        file_number = 1
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(order_path, file)
                start = time.time()

                entities2 = extract_entities.extract_entities_from_table(filename)
                wikidata_labels2 = get_info_from_wikidata.get_entity_info(entities2)
                wikidata_weighted_labels2 = label_search_wikidata.get_weighted_labels(wikidata_labels2)
                query_stop = time.time()
                query_time += query_stop - start

                r3 = relatedness.get_set_relatedness_expansion(wikidata_weighted_labels1, wikidata_weighted_labels2, n1, n2, m1, m2)
                table_relatedness[file] = r3

                calculation_stop = time.time()
                calculation_time += calculation_stop - query_stop
                print("\nCalculated relatedness for file {0} ({1}/{2})\n".format(str(file), str(file_number), len(files)))
                file_number += 1

    sorting_stop = time.time()

    sorted_relatedness = dict(sorted(table_relatedness.items(), key=lambda item: item[1], reverse=True))

    calculation_time += time.time() - sorting_stop

    print("\n")
    print("RESULT after {0} of getting labels and {1} of calculating:".format(query_time, calculation_time))
    print("Relatedness between {0} and all tables is: {1}".format(str(table1), sorted_relatedness))
    print("Top 5 related tables are:")
    i = 0
    for key, value in sorted_relatedness.items():
        if i >= 5:
            break
        i += 1
        print("{0}: {1}".format(key, value))        
        

# MAIN FUNCTION


def main(input_table, order_path, n1, n2, m1, m2, source):
    if 'wikidata' == source.lower():
        get_relatedness_for_multiple_tables_wiki(input_table, order_path,  n1=1.0, n2=1.0, m1=1.0, m2=1.0)
    elif 'dbpedia' == source.lower():
        get_relatedness_for_multiple_tables_dbpedia(input_table, order_path, n1=1.0, n2=1.0, m1=1.0, m2=1.0)   

main(input_table="data/example_dataset/countries8.csv", order_path = 'data\\example_dataset', n1=1.0, n2=1.0, m1=1.0, m2=1.0, source= "dbpedia") 
