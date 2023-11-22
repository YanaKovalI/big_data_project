import SPARQLWrapper
import json
from SPARQLWrapper import SPARQLWrapper, JSON

def get_entity_labels(entity_name):

    sparql = SPARQLWrapper('https://dbpedia.org/sparql')
    
    query = """
        SELECT DISTINCT ?relation ?relatedEntityLabel
        WHERE {{
          <http://dbpedia.org/resource/{0}> ?relation ?relatedEntity.
          ?relatedEntity rdfs:label ?relatedEntityLabel.
          FILTER(LANG(?relatedEntityLabel) = "" || LANG(?relatedEntityLabel) = "en")
          FILTER(isIRI(?relatedEntity))
        }}
    """.format(entity_name.replace(" ", "_"))


    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    result = json.loads(json.dumps(result, sort_keys=True))
    
    entity_labels = {}
    
    if result:
        # Extract and print the relations and related entity labels
        for binding in result["results"]["bindings"]:
            #relation = binding["relation"]["value"]
            related_entity_label = binding["relatedEntityLabel"]["value"]
            
            entity_labels[related_entity_label] = 1
            
            #print(f"Relation: {relation}, Related Entity Label: {related_entity_label}")
    else:
        print("Error in SPARQL query.")
        
    return entity_labels
    
def get_labels_for_set(entities):
    labels = {}
    for entity in entities:
        labels[entity] = get_entity_labels(entity)
    return labels
    
