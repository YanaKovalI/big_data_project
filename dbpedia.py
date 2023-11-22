from SPARQLWrapper import SPARQLWrapper, JSON


def get_weighted_labels(entities):
    labels = {}
    for entity in entities:
        labels[entity] = get_labels(entity)
    entity_count = 1
    for entity in labels.keys():
        weighted_labels = {}
        label_count = 1
        if labels[entity]:
            for label in labels[entity]:
                weighted_labels[label] = get_weights(label)
                label_count += 1
                print("Calculated weights for {0} labels of {1} in entity {2} of {3}".format(label_count, len(labels[entity]), entity_count, len(entities)))
        labels[entity] = weighted_labels
        print("Weighted labels for {0}: ".format(entity))
        print(weighted_labels)
        entity_count += 1
    return labels


def get_labels(entity):
    entity = entity.replace(" ", "_")
    entity = entity.capitalize()
    sparql_endpoint = "https://dbpedia.org/sparql"
    sparql_query = """SELECT DISTINCT ?relation ?relatedEntityLabel
        WHERE {{
          <http://dbpedia.org/resource/{0}> ?relation ?relatedEntity.
          ?relatedEntity rdfs:label ?relatedEntityLabel.
          FILTER(LANG(?relatedEntityLabel) = "" || LANG(?relatedEntityLabel) = "en")
        }}
    """.format(entity)
    sparql = SPARQLWrapper(endpoint=sparql_endpoint, returnFormat=JSON)
    sparql.setQuery(sparql_query)

    try:
        ret = sparql.queryAndConvert()

        labels = []
        if ret:
            for binding in ret["results"]["bindings"]:
                labels.append(binding["relatedEntityLabel"]["value"])

        print("Labels für " + entity + ": ")
        print(labels)
        return labels

    except Exception as e:
        print(e)


def get_weights(label):
    label = label.replace(" ", "_")
    sparql_endpoint = "https://dbpedia.org/sparql"
    sparql_query = """SELECT COUNT(?relatedEntityLabel)
        WHERE {{
          <http://dbpedia.org/resource/{0}> ?relation ?relatedEntity.
          ?relatedEntity rdfs:label ?relatedEntityLabel.
          FILTER(LANG(?relatedEntityLabel) = "" || LANG(?relatedEntityLabel) = "en")
        }}
    """.format(label)
    sparql = SPARQLWrapper(endpoint=sparql_endpoint, returnFormat=JSON)
    sparql.setQuery(sparql_query)

    try:
        ret = sparql.queryAndConvert()

        weight = ret["results"]["bindings"][0]["callret-0"]["value"]

        # print("Weight for label '" + label + ": " + weight)
        if int(weight) != 0:
            return 1/float(weight)
        return 0

    except Exception as e:
        print(e)
        return 0


# get_weighted_labels(["Germany", "France", "UK"])
