import dbpedia
import extract_entities
import get_info_from_wikidata
import dbpedia_test
import datetime
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
    table2 = "countries_database.csv"
    entities = extract_entities.extract_entities_from_table(table)
    entities2 = extract_entities.extract_entities_from_table(table2)
    information = get_info_from_wikidata.get_entity_info(entities)
    information2 = get_info_from_wikidata.get_entity_info(entities2)
    result = label_search_wikidata.get_weighted_labels(information)
    result2 = label_search_wikidata.get_weighted_labels(information2)
    r = relatedness.get_average_pair(result, result2)
    relatedness_between_sets = relatedness.get_relatedness_sets(result,result2)
    print("\n")
    print("RESULT:")
    print("Average relatedness between " + str(table) + " and " + str(table2) + ": " + str(relatedness_between_sets))
    
# wikidata_main()

def dbpedia_main():
    # table1 = "data/zoo_data/zoo2.csv"s
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
    # table1 = "data/zoo_data/zoo2.csv"
    # table2 = "data/zoo_data/zoo3.csv"
    table1 = "countries_database.csv"
    table2 = "countries_database.csv"
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    dbpedia_labels1 = dbpedia.get_weighted_labels(entities1)
    dbpedia_labels2 = dbpedia.get_weighted_labels(entities2)
    print(dbpedia_labels1)
    print(dbpedia_labels2)
    # r = relatedness.get_average_pair(dbpedia_labels1, dbpedia_labels2)
    r = relatedness.get_set_relatedness(dbpedia_labels1, dbpedia_labels2)
    r2 = relatedness.get_relatedness_sets(dbpedia_labels1, dbpedia_labels2)
    print("\n")
    print("RESULT after {0} of calculation:".format(datetime.datetime.now().replace(microsecond=0) - start_time))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(r))


weighted_dbpedia_main()
