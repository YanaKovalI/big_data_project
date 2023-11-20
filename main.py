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
    #look for requests for each entity
    # for entity, label_list in information.items():
    #     for label in label_list:
    #         res = label_search_wikidata.get_number_of_entities_for_label(label)
    #         print(f"for label {label} RESULT: {res} \n\n\n")
    result = label_search_wikidata.get_domain_size_of_labels(information)
    print(result)  
wikidata_main()