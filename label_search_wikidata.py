from networkx import information_centrality
import requests
class SPARQLQueryDispatcher:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        

    def query(self, sparql_query):
        full_url = f"{self.endpoint}?query={requests.utils.quote(sparql_query)}"
        headers = {'Accept': 'application/sparql-results+json'}

        response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None


def get_number_of_entities_for_label(label):
# Endpoint URL
    endpoint_url = 'https://query.wikidata.org/sparql'

    # SPARQL Query
    sparql_query = f"""
    SELECT ?item ?itemLabel
    WHERE {{
        ?item rdfs:label "{label}"@en.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """
    # Create an instance of SPARQLQueryDispatcher
    query_dispatcher = SPARQLQueryDispatcher(endpoint_url)

    # Execute the SPARQL query
    query_results = query_dispatcher.query(sparql_query)
    if query_results is None:
        number_of_entities = 1
    else:    
        items = query_results.get("results", {}).get("bindings", {})
        number_of_entities = len(items)
    return number_of_entities
    

def get_domain_size_of_labels(information):
    for entity, label_list in information.items():
        label_domain = {}
        for label in label_list:
            label_domain[label] = get_number_of_entities_for_label(label)
        information[entity] = label_domain   
    return information

def get_weighted_labels(information):
    for entity, label_list in information.items():
        label_weights = {}
        for label in label_list:
            num_entities = get_number_of_entities_for_label(label)
            if num_entities != 0:  # Check if the number of entities is not zero
                label_weights[label] = 1 / num_entities
            else:
                label_weights[label] = 0  # Or handle this case as per your requirement
        information[entity] = label_weights
    return information