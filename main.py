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
    table1 = "countries_database.csv"
    table2 = "countries_database.csv"
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    # check if we have already query results for some entities
    # also check if json file is not empty  
    try:
        with open(stored_results, 'r') as json_file:
            file_content = json_file.read()    # Check if file content is not empty
            if file_content.strip():
                data = json.loads(file_content)   #save json file as dictionary
            else:
                data = {}  #json file is empty
    except FileNotFoundError:
        print("File not found.")
        data = {}

    # check if we have already query results for some entities   
    # data_dict is a list of ditcionaries     
    def check_entities(entities, data_dict : dict):
        entities_in_data = {}
        entities_not_in_data = []
        for entity in entities:
            found = False  # Flag to track if entity is found in any dictionary
            for data in data_dict:
                if entity in data.keys():
                    # Entity exists in the dictionary
                    entities_in_data[entity] = data[entity]  # Store entity key and its value
                    found = True
                    break   # Break out of the loop once entity is found in a dictionary
            if not found: # Entity doesn't exist in the dictionary
                entities_not_in_data.append(entity) # Collect entities not present
        print(f"Entities in data stored : {entities_in_data}")
        print(f"Entities that was not in the data {entities_not_in_data}")
        return entities_in_data, entities_not_in_data

    entities_in_data_1, entities_not_in_data_1 = check_entities(entities1, data)
    entities_in_data_2, entities_not_in_data_2 = check_entities(entities2, data)
    data_list =  []
    if len(entities_not_in_data_1) > 0:        
        information1 = get_info_from_wikidata.get_entity_info(entities_not_in_data_1)
        result1 = label_search_wikidata.get_weighted_labels(information1)
        data_list.append(result1)
        print(f"Entities in data: {entities_in_data_1}, entities not in data, that was queries : {result1}")
        #then we need to merge finded entities labels and not founded entitites labels results
        combined1 = {**entities_in_data_1, **result1} 
    if len(entities_not_in_data_2) > 0:    
        information2 = get_info_from_wikidata.get_entity_info(entities_not_in_data_2)
        result2 = label_search_wikidata.get_weighted_labels(information2)
        data_list.append(result2)
        print(f"Entities in data: {entities_in_data_2}, entities not in data, that was queries : {result2}")
        #then we need to merge finded entities labels and not founded entitites labels results
        combined2 = {**entities_in_data_2, **result2} 
    
    # Save all dictionaries to a single JSON file
    # Open the file in append mode ('a')
    # Read existing data from the file if it exists
    existing_data = []
    try:
        with open(stored_results, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        pass  # File doesn't exist yet, so no existing data

    # Merge existing data with new data
    merged_data = existing_data + data_list

    # Write the merged data back to the file
    with open(stored_results, 'w') as json_file:
        json.dump(merged_data, json_file, indent=4)


    if len(entities_not_in_data_1) > 0 & len(entities_not_in_data_2) > 0:
        r = relatedness.get_average_pair(combined1, combined2)   
        relatedness_between_sets = relatedness.get_relatedness_sets(combined1, combined2)
    if len(entities_not_in_data_1) > 0 & len(entities_not_in_data_2) == 0:
        r = relatedness.get_average_pair(combined1, entities_in_data_2)   
        relatedness_between_sets = relatedness.get_relatedness_sets(combined1, entities_in_data_2)
    if len(entities_not_in_data_1) == 0 & len(entities_not_in_data_2) > 0:
        r = relatedness.get_average_pair(entities_in_data_1, combined2)   
        relatedness_between_sets = relatedness.get_relatedness_sets(entities_in_data_1, combined2)
    if len(entities_not_in_data_1) == 0 & len(entities_not_in_data_2) == 0:
        #print(f"\n WE CALCULATE RELATEDNESS BETWEEN {entities_in_data_1} AND {entities_in_data_2}")
        r = relatedness.get_average_pair(entities_in_data_1, entities_in_data_2)   
        relatedness_between_sets = relatedness.get_relatedness_sets(entities_in_data_1, entities_in_data_2)
    
    print("\n")
    print("RESULT after {0} of calculation:".format(datetime.datetime.now().replace(microsecond=0) - start_time))
    print("Average relatedness between " + str(table1) + " and " + str(table2) + ": " + str(relatedness_between_sets))


wikidata_main()


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


#weighted_dbpedia_main()


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
