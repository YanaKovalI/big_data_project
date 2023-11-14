import read_webisadb
import extract_entities


def dot_product(vector1, vector2):
    product = 0
    for label in vector1:
        label2 = vector2.get(label)
        if label2 is not None:
            product += vector1.get(label) * vector2.get(label)
    return product


def get_relatedness(table1, table2):
    entities1 = extract_entities.extract_entities_from_table(table1)
    entities2 = extract_entities.extract_entities_from_table(table2)
    labels1 = {}
    labels2 = {}
    for entity in entities1:
        labels1[entity] = read_webisadb.find_labels(entity)
    for entity in entities2:
        labels2[entity] = read_webisadb.find_labels(entity)


A = {"a": 1, "b": 1, "c": 2}
B = {"d": 1, "e": 1, "f": 1}
C = {"b": 1, "c": 1.5, "e": 4}

print("A@B: " + str(dot_product(A, B)))
print("B@C: " + str(dot_product(B, C)))
print("A@C: " + str(dot_product(A, C)))
