from SPARQLWrapper import SPARQLWrapper, JSON

def get_labels(entity):
    query_results = query_webisa(entity)
    labels = format_query_results(query_results)
    print(labels)


def query_webisa(entity, confidence=0.75):
    sparql_endpoint = "http://webisa.webdatacommons.org/sparql"
    sparql_query = """PREFIX isa: <http://webisa.webdatacommons.org/concept/>
    PREFIX isaont: <http://webisa.webdatacommons.org/ontology#> 
    SELECT ?hypernymLabel ?hyponymLabel ?confidence
    WHERE{
        GRAPH ?g {
            isa:_""" + entity.lower() + """_ skos:broader ?hyponym.
        }
        isa:_""" + entity.lower() + """_ rdfs:label ?hypernymLabel.
        ?hyponym rdfs:label ?hyponymLabel.
        ?g isaont:hasConfidence ?confidence.
        FILTER(?confidence >= """ + str(confidence) + """)
    }
    ORDER BY DESC(?confidence)"""

    sparql = SPARQLWrapper(endpoint=sparql_endpoint, returnFormat=JSON)
    sparql.setQuery(sparql_query)

    try:
        ret = sparql.queryAndConvert()

        for r in ret["results"]["bindings"]:
            print(r)
        return ret["results"]["bindings"]

    except Exception as e:
        print(e)


def format_query_results(query_results):
    labels = {}
    for result in query_results:
        labels[result["hyponymLabel"]["value"]] = result["confidence"]["value"]
    return labels


get_labels("Germany")
