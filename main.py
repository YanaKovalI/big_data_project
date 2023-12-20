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


def wikidata_main():
    start_time = datetime.datetime.now().replace(microsecond=0)
    stored_results = 'sparql_queries_results.json'
    table1 = "data/example_dataset/countries0.csv"
    table2 = "data/example_dataset/countries2.csv"
    info1, info2 =  get_info_from_wikidata.get_info_with_check(stored_results_json=stored_results,table1=table1,table2=table2)
    r = relatedness.get_average_pair(info1, info2)   
    relatedness_between_sets = relatedness.get_relatedness_sets(info1, info2)
    print("\n")
    print("RESULT after {0} of calculation:".format(datetime.datetime.now().replace(microsecond=0) - start_time))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(relatedness_between_sets))

# wikidata_main()


def weighted_dbpedia_main():
    start_time = datetime.datetime.now().replace(microsecond=0)
    table1 = "data/example_dataset/countries8.csv"
    table2 = "data/example_dataset/countries2.csv"
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    dbpedia_labels1 = dbpedia.get_weighted_labels(entities1)
    dbpedia_labels2 = dbpedia.get_weighted_labels(entities2)
    print(dbpedia_labels1)
    print(dbpedia_labels2)
    time_labels = datetime.datetime.now().replace(microsecond=0) - start_time
    r = relatedness.get_average_pair(dbpedia_labels1, dbpedia_labels2)
    r2 = relatedness.get_set_relatedness(dbpedia_labels1, dbpedia_labels2)
    r3 = relatedness.get_set_relatedness_expansion(dbpedia_labels1, dbpedia_labels2)
    time_calculation = datetime.datetime.now().replace(microsecond=0) - time_labels - start_time
    print("\n")
    print("RESULT after {0} of getting labels and {1} of calculating:".format(time_labels, time_calculation))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r2))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r3))


# weighted_dbpedia_main()


def get_relatedness_for_multiple_tables(table1="data/example_dataset/countries8.csv"):
    labelsdb.init_database()

    query_time = 0
    calculation_time = 0

    entities1 = extract_entities.extract_entities_from_table(table1)
    dbpedia_labels1 = dbpedia.get_weighted_labels(entities1)
    table_relatedness = dict()

    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, 'data\\example_dataset')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join('data\\example_dataset', file)

                start = time.time()

                entities2 = extract_entities.extract_entities_from_table(filename)
                dbpedia_labels2 = dbpedia.get_weighted_labels(entities2)

                query_stop = time.time()
                query_time += query_stop - start

                r3 = relatedness.get_set_relatedness_expansion(dbpedia_labels1, dbpedia_labels2)
                table_relatedness[file] = r3

                calculation_stop = time.time()
                calculation_time += calculation_stop - query_stop

    sorting_stop = time.time()

    sorted_relatedness = dict(sorted(table_relatedness.items(), key=lambda item: item[1], reverse=True))

    calculation_time += time.time() - sorting_stop

    print("\n")
    print("RESULT after {0} of getting labels and {1} of calculating:".format(query_time, calculation_time))
    print("Relatedness between {0} and all tables is: {1}".format(str(table1), sorted_relatedness))
    print("Top 5 related tables are:")
    i = 0
    for key, value in sorted_relatedness.items():
        if i >= 4:
            break
        i += 1
        print("{0}: {1}".format(key, value))


get_relatedness_for_multiple_tables()   
# def main(input_table, order_path, n1, n2, m1, m2, quelle):



