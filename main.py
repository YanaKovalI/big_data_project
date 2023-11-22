import dbpedia
import extract_entities
import get_info_from_wikidata
import dbpedia_test
import datetime
import pandas as pd
import requests
import query_webisa
import relatedness
import label_search_wikidata
from label_search_wikidata import SPARQLQueryDispatcher


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
    table = "countries_database.csv"
    entities = extract_entities.extract_entities_from_table(table)
    information = get_info_from_wikidata.get_entity_info(entities)
    result = label_search_wikidata.get_weighted_labels(information)
    r = relatedness.get_average_pair(result, result)
    print("\n")
    print("RESULT:")
    print("Average relatedness between " + str(table) + " and " + str(table) + ": " + str(r))
    
#wikidata_main()

def dbpedia_main():
    # table1 = "data/zoo_data/zoo2.csv"
    # table2 = "data/zoo_data/zoo3.csv"
    table1 = "countries_database.csv"
    table2 = "countries_database.csv"
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    dbpedia_labels1 = dbpedia_test.get_labels_for_set(entities1)
    dbpedia_labels2 = dbpedia_test.get_labels_for_set(entities2)
    print(dbpedia_labels1)
    print(dbpedia_labels2)
    r = relatedness.get_average_pair(dbpedia_labels1, dbpedia_labels2)
    print("\n")
    print("RESULT:")
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r))


# dbpedia_main()


def weighted_dbpedia_main():
    start_time = datetime.datetime.now().replace(microsecond=0)
    table1 = "data/zoo_data/zoo2.csv"
    table2 = "data/zoo_data/zoo3.csv"
    # table1 = "countries_database.csv"
    # table2 = "countries_database.csv"
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    dbpedia_labels1 = dbpedia.get_weighted_labels(entities1)
    dbpedia_labels2 = dbpedia.get_weighted_labels(entities2)
    print(dbpedia_labels1)
    print(dbpedia_labels2)
    r = relatedness.get_average_pair(dbpedia_labels1, dbpedia_labels2)
    print("\n")
    print("RESULT after {0} of calculation:".format(datetime.datetime.now().replace(microsecond=0) - start_time))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r))


weighted_dbpedia_main()
