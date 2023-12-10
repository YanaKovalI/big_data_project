import json

from SPARQLWrapper import SPARQLWrapper, JSON

cache = dict()


def get_weighted_labels(entities, limit=99999):
    labels = {}
    entities_not_in_csv = []
    for entity in entities:
        try:
            with open('dbpedia_labels.json', 'r') as file:
                data = json.load(file)
                if entity in data.keys():
                    labels[entity] = data[entity]
                else:
                    entities_not_in_csv.append(entity)
                    labels[entity] = get_labels_by_query(entity, limit)


        except Exception as e:
            entities_not_in_csv.append(entity)
            labels[entity] = get_labels_by_query(entity, limit)

    entity_count = 1
    for entity in entities_not_in_csv:
        entity_labels = labels[entity]

        weighted_labels = get_weighted_labels_in_chunks(entity_labels)

        # if big queries did not work, query for each label individually
        if entity_labels and not weighted_labels:
            weighted_labels = {}
            label_count = 1
            for label in entity_labels:
                weighted_labels[label] = get_weights(label)
                label_count += 1
                print("Calculated weights for {0} labels of {1} in entity {2} of {3}".format(label_count,
                                                                                             len(entity_labels),
                                                                                             entity_count,
                                                                                             len(entities)))
        labels[entity] = weighted_labels
        print("Weighted labels for {0}: ".format(entity))
        print(weighted_labels)
        entity_count += 1
        save_to_json_file(entity, weighted_labels)
    return labels


def save_to_json_file(entity, weighted_labels):
    with open('dbpedia_labels.json', 'r') as infile:
        try:
            data = json.load(infile)
            data = data | {entity: weighted_labels}
            with open('dbpedia_labels.json', 'w') as outfile:
                json.dump(data, outfile)
        except Exception as e:
            with open('dbpedia_labels.json', 'w') as outfile:
                json.dump({entity: weighted_labels}, outfile)


def get_json_dict():
    json_file = open('dbpedia_makeshift_db.json')
    json_str = json_file.read()
    json_data = json.loads(json_str)[0]
    return json_data


def get_weighted_labels_in_chunks(labels):
    entity_labels_chunks = list()
    for i in range(0, len(labels), 100):
        entity_labels_chunks.append(labels[i:i + 100])
    weighted_labels_chunks = list()
    for chunk in entity_labels_chunks:
        weighted_labels_chunks.append(get_weights_with_one_query(chunk))
    weighted_labels = dict()
    for chunk in weighted_labels_chunks:
        weighted_labels = weighted_labels | chunk
    return weighted_labels


def get_labels_by_query(entity, limit):
    entity = entity.replace(" ", "_")
    sparql_endpoint = "https://dbpedia.org/sparql"
    sparql_query = """SELECT DISTINCT ?relation ?relatedEntityLabel
        WHERE {{
          <http://dbpedia.org/resource/{0}> ?relation ?relatedEntity.
          ?relatedEntity rdfs:label ?relatedEntityLabel.
          FILTER(LANG(?relatedEntityLabel) = "" || LANG(?relatedEntityLabel) = "en")
        }}
        LIMIT {1}
    """.format(entity, limit)
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
        return dict()


def get_weights_with_one_query(labels):
    if not labels:
        return dict()
    query_argument = "<http://dbpedia.org/resource/" + labels[0].replace(" ", "_") + ">"
    for label in labels[1:]:
        label = "<http://dbpedia.org/resource/" + label.replace(" ", "_") + ">"
        query_argument = query_argument + ", " + label

    sparql_endpoint = "https://dbpedia.org/sparql"
    sparql_query = """SELECT DISTINCT ?entity (COUNT(?relatedEntityLabel) as ?domain_size)
        WHERE {{
          ?entity ?relation ?relatedEntity.
          ?relatedEntity rdfs:label ?relatedEntityLabel.
          FILTER(LANG(?relatedEntityLabel) = "en" && ((?entity ) in ({0})))
        }}
    """.format(query_argument)
    sparql = SPARQLWrapper(endpoint=sparql_endpoint, returnFormat=JSON)
    sparql.setQuery(sparql_query)

    try:
        ret = sparql.queryAndConvert()

        weights = dict()
        if ret:
            for binding in ret["results"]["bindings"]:
                entity = binding['entity']['value'].removeprefix('http://dbpedia.org/resource/')
                domain_size = binding['domain_size']['value']
                weights[entity] = 1 / float(domain_size)
        return weights

    except Exception as e:
        print(e)
        return dict()


def get_weights(label):
    label = label.replace(" ", "_")
    weight = cache.get(label)
    if weight is not None:
        return weight
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
            weight = 1 / float(weight)
            cache[label] = weight
            return weight
        return 0

    except Exception as e:
        print(e)
        return 0
