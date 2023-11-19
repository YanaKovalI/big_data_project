import extract_entities
import get_info_from_wikidata
import pandas as pd
import requests
import query_webisa
import relatedness
import label_search_wikidata
from label_search_wikidata import SPARQLQueryDispatcher
        
def main():
    table = "countries_database.csv"
    entities = extract_entities.extract_entities_from_table(table)
    webisadb_labels = query_webisa.get_labels_for_set(entities)      #weighted labels
    r = relatedness.get_average_pair(webisadb_labels, webisadb_labels)
    print("\n")
    print("RESULT:")
    print("Average relatedness between " + str(table) + " and " + str(table) + ": " + str(r))

#main()

def wikidata_main():
    table = "countries_database.csv"
    entities = extract_entities.extract_entities_from_table(table)
    information = get_info_from_wikidata.get_entity_info(entities)
    result = label_search_wikidata.get_number_of_entities_for_label(information)
    print(result)
    # r = relatedness.get_average_pair(wikidata_labels,wikidata_labels)
    # print("\n")
    # print("RESULT:")
    # print("Average relatedness between " + str(table) + " and " + str(table) + ": " + str(r))
    
wikidata_main()    
