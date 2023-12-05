import os

import dbpedia
import extract_entities
import get_info_from_wikidata
import datetime
import query_webisa
import relatedness
import label_search_wikidata
from label_search_wikidata import SPARQLQueryDispatcher
import json


def webisa_main():
    table1 = "data/zoo_data/zoo2.csv"
    table2 = "data/zoo_data/zoo3.csv"
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    webisadb_labels1 = query_webisa.get_labels_for_set(entities1)  # weighted labels
    webisadb_labels2 = query_webisa.get_labels_for_set(entities2)  # weighted labels
    r = relatedness.get_average_pair(webisadb_labels1, webisadb_labels2)
    print("\n")
    print("RESULT:")
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r))


# webisa_main()

def wikidata_main():
    start_time = datetime.datetime.now().replace(microsecond=0)
    stored_results = 'sparql_queries_results.json'
    table = "countries_database.csv"
    table2 = "countries_database.csv"
    entities = extract_entities.extract_entities_from_table(table)
    entities2 = extract_entities.extract_entities_from_table(table2)
    information = get_info_from_wikidata.get_entity_info(entities)
    information2 = get_info_from_wikidata.get_entity_info(entities2)
    data_list =  []
    data_list.append(information)
    data_list.append(information2)
    # Save all dictionaries to a single JSON file
    with open('sparql_queries_results.json', 'w') as json_file:
        json.dump(data_list, json_file, indent=4)
    result = label_search_wikidata.get_weighted_labels(information)
    result2 = label_search_wikidata.get_weighted_labels(information2)
    r = relatedness.get_average_pair(result, result2)
    relatedness_between_sets = relatedness.get_relatedness_sets(result, result2)
    print("\n")
    print("RESULT after {0} of calculation:".format(datetime.datetime.now().replace(microsecond=0) - start_time))
    print("Average relatedness between " + str(table) + " and " + str(table2) + ": " + str(relatedness_between_sets))


# wikidata_main()


def weighted_dbpedia_main():
    start_time = datetime.datetime.now().replace(microsecond=0)
    # table1 = "data/zoo_data/zoo2.csv"
    # table2 = "data/zoo_data/zoo3.csv"
    # table1 = "countries_database.csv"
    # table2 = "countries_database.csv"
    table1 = "data/example_dataset/targets4.csv"
    table2 = "data/example_dataset/targets8.csv"
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    dbpedia_labels1 = dbpedia.get_weighted_labels(entities1)
    dbpedia_labels2 = dbpedia.get_weighted_labels(entities2)
    print(dbpedia_labels1)
    print(dbpedia_labels2)
    time_labels = datetime.datetime.now().replace(microsecond=0) - start_time
    # r = relatedness.get_average_pair(dbpedia_labels1, dbpedia_labels2)
    r = relatedness.get_set_relatedness(dbpedia_labels1, dbpedia_labels2)
    r2 = relatedness.get_relatedness_sets(dbpedia_labels1, dbpedia_labels2)
    time_calculation = datetime.datetime.now().replace(microsecond=0) - time_labels - start_time
    print("\n")
    print("RESULT after {0} of getting labels and {1} of calculating:".format(time_labels, time_calculation))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r))


weighted_dbpedia_main()


def get_relatedness_for_multiple_tables(table1=""):
    start_time = datetime.datetime.now().replace(microsecond=0)

    dirname = os.path.dirname(__file__)
    directory = os.path.join(dirname, 'data\\example_dataset')
    print(directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join('data\\example_dataset', file)
                # print(str(filename))
                entities = extract_entities.extract_entities_from_table(filename)
                # print(entities)


# get_relatedness_for_multiple_tables()


def wiki_plus_dbpedia():

    start_time = datetime.datetime.now().replace(microsecond=0)
    # table1 = "data/zoo_data/zoo2.csv"
    # table2 = "data/zoo_data/zoo3.csv"
    table1 = "countries_database.csv"
    table2 = "countries_database.csv"
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    wikidata_labels1 = get_info_from_wikidata.get_entity_info(table1)
    wikidata_labels2 = get_info_from_wikidata.get_entity_info(table2)
    wikidata_weighted_labels1 = label_search_wikidata.get_weighted_labels(wikidata_labels1)
    wikidata_weighted_labels2 = label_search_wikidata.get_weighted_labels(wikidata_labels2)
    dbpedia_labels1 = dbpedia.get_weighted_labels(entities1)
    dbpedia_labels2 = dbpedia.get_weighted_labels(entities2)
    #combine labels
    combined_labels1 = {**wikidata_weighted_labels1, **dbpedia_labels1}
    combined_labels2 = {**wikidata_weighted_labels2, **dbpedia_labels2} 
    #print(combined_labels1)
    #print(combined_labels2)
    # r = relatedness.get_average_pair(dbpedia_labels1, dbpedia_labels2)
    r = relatedness.get_set_relatedness(combined_labels1, combined_labels2)
    r2 = relatedness.get_relatedness_sets(combined_labels1, combined_labels2)
    print("\n")
    print("RESULT after {0} of calculation:".format(datetime.datetime.now().replace(microsecond=0) - start_time))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r2))

#wiki_plus_dbpedia()
