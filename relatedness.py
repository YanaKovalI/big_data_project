import extract_entities


def dot_product(vector1: dict, vector2: dict) -> float:
    product = 0
    for label in vector1:
        label2 = vector2.get(label)
        if label2 is not None:
            product += float(vector1.get(label)) * float(vector2.get(label))
    return product


def get_relatedness(label_set1: dict, label_set2: dict) -> float:
    dot_products = {}
    relatedness = 0

    for entity1 in label_set1:
        for entity2 in label_set2:
            key = entity1 + "->" + entity2
            dot_products[key] = (dot_product(label_set1[entity1], label_set2[entity2]))
            relatedness += dot_products[key]

    return relatedness


def get_average_pair(label_set1: dict, label_set2: dict) -> float:
    r = get_relatedness(label_set1, label_set2)
    count1 = len(label_set1)
    count2 = len(label_set2)
    return (1/(count1*count2))*r
