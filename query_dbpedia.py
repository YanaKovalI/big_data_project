import requests

# SPARQL query
sparql_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbpedia: <http://dbpedia.org/resource/>
PREFIX dbp-ont: <http://dbpedia.org/ontology/>

SELECT ?link
WHERE {
  dbpedia:Berlin rdfs:seeAlso ?link.
}
"""

# DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Set the request headers
headers = {
    "Accept": "application/json",
    "User-Agent": "HaukeGS"
}

# Set the query parameters
params = {
    "query": sparql_query,
    "format": "json"
}

# Send the SPARQL query request
response = requests.get(sparql_endpoint, params=params, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    results = response.json()

    # Extract and print the links
    for result in results["results"]["bindings"]:
        link = result["link"]["value"]
        print(link)

else:
    print(f"Error: {response.status_code}, {response.text}")