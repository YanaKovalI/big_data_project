import get_info_from_wikidata
import pandas as pd

table = "countries_database.csv"
domain_labels = get_info_from_wikidata.get_domain_size_labels(table)
print(domain_labels)
