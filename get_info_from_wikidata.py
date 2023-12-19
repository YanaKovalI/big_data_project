import requests
import pandas as pd
import extract_entities
import json
import re
import label_search_wikidata

# input_table = pd.read_csv(csv_file_table)
# entities = extract_entities.extract_entities_from_table(input_table)

#as an input should be a csv_file, return a dictionary entities with lists of weights
def get_entity_info(entities):
    url = "https://www.wikidata.org/w/api.php"

    results = []

    for entity in entities:
        params = {
        "action" : "wbsearchentities",
        "language" : "en",
        "format" : "json",
        "search" : entity
    }
        data =  requests.get(url, params = params)
        results.append(data.json())
 

    information = {}  # Initialize the information dictionary "entity" : [list of labels]

    for entity, result in zip(entities, results):
        labels = []  # Initialize a list to store labels for each entity
        for item in result.get("search", []):
            label = item.get("display", {}).get("label", {}).get("value")
            if label not in labels:
                labels.append(label)
        # Store the labels list for each entity
        information[entity] = labels
    return information

def get_info_with_check(stored_results_json,table1,table2):

    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)

    try:
        with open(stored_results_json, 'r') as json_file:
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
    data_list =  [] #list of new query results for entities

    if len(entities_not_in_data_1) > 0 & len(entities_in_data_1) > 0:        
        information1 = get_entity_info(entities_not_in_data_1)
        result1 = label_search_wikidata.get_weighted_labels(information1)
        data_list.append(result1)
        print(f"Entities in data: {entities_in_data_1}, entities not in data, that were queried : {result1}")
        #then we need to merge finded entities labels and not founded entitites labels results
        info1 = {**entities_in_data_1, **result1} 
    if len(entities_not_in_data_1) > 0 & len(entities_in_data_1) == 0:        
        information1 = get_entity_info(entities_not_in_data_1)
        result1 = label_search_wikidata.get_weighted_labels(information1)
        data_list.append(result1)
        print(f"Entities in data: {entities_in_data_1}, entities not in data, that were queried : {result1}")
        #then we need to merge finded entities labels and not founded entitites labels results
        info1 = result1.copy()
    if len(entities_not_in_data_1) == 0:        
        print(f"Entities in data: {entities_in_data_1},  no entities not in data, that were queried")
        #then we need to merge finded entities labels and not founded entitites labels results
        info1 = entities_in_data_1.copy()

    if len(entities_not_in_data_2) > 0 & len(entities_in_data_2) > 0:    
        information2 = get_entity_info(entities_not_in_data_2)
        result2 = label_search_wikidata.get_weighted_labels(information2)
        data_list.append(result2)
        print(f"Entities in data: {entities_in_data_2}, entities not in data, that were queried : {result2}")
        #then we need to merge finded entities labels and not founded entitites labels results
        info2 = result2.copy() 
    if len(entities_not_in_data_2) > 0 & len(entities_in_data_2) == 0:    
        information2 = get_entity_info(entities_not_in_data_2)
        result2 = label_search_wikidata.get_weighted_labels(information2)
        data_list.append(result2)
        print(f"Entities in data: {entities_in_data_2}, entities not in data, that were queried : {result2}")
        #then we need to merge finded entities labels and not founded entitites labels results
        info2 = {**entities_in_data_2, **result2}
    if len(entities_not_in_data_2) == 0:        
        print(f"Entities in data: {entities_in_data_2},  no entities not in data, that were queried")
        #then we need to merge finded entities labels and not founded entitites labels results
        info2 = entities_in_data_2.copy()        
    
    # Save all dictionaries to a single JSON file
    # Open the file in append mode ('r')
    # Read existing data from the file if it exists
    existing_data = []
    try:
        with open(stored_results_json, 'r') as json_file:
            file_content = json_file.read()
            if file_content.strip():
                existing_data = json.loads(file_content)
            else:
                existing_data = []        
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON data.")    

    # Merge existing data with new data
    merged_data = existing_data + data_list

    # Write the merged data back to the file
    with open(stored_results_json, 'w') as json_file:
        json.dump(merged_data, json_file, indent=4)

    return info1,info2    