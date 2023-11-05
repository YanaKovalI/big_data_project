import requests
import pandas as pd

url = "https://www.wikidata.org/w/api.php"

input_table = pd.read_csv("countries_database.csv")

#extract entities from the first column
def extract_entities_from_table(table):
        entities = table.iloc[:, 0].tolist()
        return entities

#query = input("Enter entity:")
entities = extract_entities_from_table(input_table)
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


# Now you can work with the results as needed, for example, print them all:
for result in results:
    print(f"NEW ENTITY {result}\n\n\n")