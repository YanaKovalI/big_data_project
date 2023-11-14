import extract_entities
import get_info_from_wikidata
import pandas as pd

import query_webisa
import relatedness


def main():
    table = "countries_database.csv"
    # domain_labels = get_info_from_wikidata.get_domain_size_labels(table)
    # print(domain_labels)

    dataset = pd.read_csv(table)
    entities = extract_entities.extract_entities_from_table(dataset)
    webisadb_labels = query_webisa.get_labels_for_set(entities)
    r = relatedness.get_average_pair(webisadb_labels, webisadb_labels)
    print("\n")
    print("RESULT:")
    print("Average relatedness between " + str(table) + " and " + str(table) + ": " + str(r))

main()