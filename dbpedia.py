import json

from SPARQLWrapper import SPARQLWrapper, JSON

import labelsdb

cache = dict()


def get_weighted_labels(entities, limit=99999):
    entity_number = 1
    entities_weighted_labels = dict()
    entity_labels = dict()
    for entity in entities:
        try:
            weighted_labels = labelsdb.get_weighted_labels(entity)
            if weighted_labels is not None:
                entities_weighted_labels[entity] = weighted_labels
                print("Calculated {0} weighted labels for entity {1} ({2}/{3})".format(len(weighted_labels), entity, entity_number, len(entities)))
                entity_number += 1
            else:
                entity_labels[entity] = get_labels_by_query(entity, limit)

        except Exception as e:
            entity_labels[entity] = get_labels_by_query(entity, limit)

    entities_not_in_db = list(entity_labels.keys())
    for entity in entities_not_in_db:
        labels = entity_labels[entity]

        if labels:
            weighted_labels = get_weights(labels)
            labelsdb.put_weighted_labels(entity, weighted_labels)
        else:
            weighted_labels = dict()
            labelsdb.put_labelless_entity(entity)

        entities_weighted_labels[entity] = weighted_labels
        print("Calculated {0} weighted labels for entity {1} ({2}/{3})".format(len(weighted_labels), entity, entity_number, len(entities)))
        entity_number += 1
    return entities_weighted_labels


def get_weights(labels):
    weighted_labels = dict()
    for label in labels:
        try:
            weight = labelsdb.get_weight(label)
            if weight:
                weighted_labels[label] = weight
        except Exception as e:
            print(e)
    labels2 = list(set(labels) - set(weighted_labels.keys()))
    if labels:
        weighted_labels_chunked = get_weighted_labels_in_chunks(labels2)
        if weighted_labels_chunked:
            weighted_labels = weighted_labels | weighted_labels_chunked
        else:
            for label in labels2:
                weighted_labels[label] = get_weights_for_single_label(label)
    return weighted_labels


def get_weighted_labels_in_chunks(labels):
    if not labels:
        return dict()
    try:
        entity_labels_chunks = list()
        for i in range(0, len(labels), 100):
            entity_labels_chunks.append(labels[i:i + 100])
        weighted_labels = dict()
        for chunk in entity_labels_chunks:
            weighted_labels = weighted_labels | get_weights_with_one_query(chunk)
        return weighted_labels
    except Exception as e:
        print(e)
        tuples = [(l, 0) for l in labels]
        return dict(tuples)


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

        return list(set(labels))

    except Exception as e:
        print(e)
        return list()


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


def get_weights_for_single_label(label):
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

        if int(weight) != 0:
            weight = 1 / float(weight)
            cache[label] = weight
            return weight
        return 0

    except Exception as e:
        print(e)
        return 0
