import extract_entities


def dot_product(vector1: dict, vector2: dict) -> float:
    product = 0
    for label in vector1:
        if label in vector2.keys():
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
            # print(dot_products)
    return relatedness


# formula 4
def get_average_pair(label_set1: dict, label_set2: dict) -> float:
    r = get_relatedness(label_set1, label_set2)
    count1 = len(label_set1)
    count2 = len(label_set2)
    if count2 * count2 == 0:
        return 0
    return (1 / (count1 * count2)) * r


# formula 5, we multiply get_avg_pairs by size of Entity set 2
def get_sum_pair(label_set1: dict, label_set2: dict) -> float:
    avg_pairs_result = get_average_pair(label_set1, label_set2)
    return avg_pairs_result * len(label_set2)


def get_weighted_entity_set(label_set: dict) -> dict:
    weighted_entity_set = dict()
    for entity in label_set:
        labels = label_set[entity]
        for label in labels:
            if label in weighted_entity_set.keys():
                weighted_entity_set[label] += labels[label]
            else:
                weighted_entity_set[label] = labels[label]
    for label in weighted_entity_set.keys():
        weighted_entity_set[label] /= len(label_set)
    return weighted_entity_set


def get_weighted_expansion_entity_set(label_set: dict, n=1.0, m=1.0) -> dict:
    weighted_expansion_entity_set = dict()
    for entity in label_set:
        labels = label_set[entity]
        for label in labels:
            if label in weighted_expansion_entity_set.keys():
                weighted_expansion_entity_set[label] += labels[label]
            else:
                weighted_expansion_entity_set[label] = labels[label]
    for label in weighted_expansion_entity_set.keys():
        weighted_expansion_entity_set[label] = pow(weighted_expansion_entity_set[label], n) / pow(len(label_set), m)
    return weighted_expansion_entity_set


def get_set_relatedness(label_set1: dict, label_set2: dict) -> float:
    weighted_entity_set1 = get_weighted_entity_set(label_set1)
    weighted_entity_set2 = get_weighted_entity_set(label_set2)
    product = dot_product(weighted_entity_set1, weighted_entity_set2)
    return product


def get_set_relatedness_expansion(label_set1: dict, label_set2: dict, n1=1.0, n2=1.0, m1=1.0, m2=1.0) -> float:
    weighted_entity_set1 = get_weighted_expansion_entity_set(label_set1, n1, m1)
    weighted_entity_set2 = get_weighted_expansion_entity_set(label_set2, n2, m2)
    product = dot_product(weighted_entity_set1, weighted_entity_set2)
    return product


def get_relatedness_sets(label_set1: dict, label_set2: dict) -> float:
    relatedness = 0
    labels_w_from_first_set = {}
    labels_w_from_second_set = {}
    # get all labels & weights from all entities from entity set 1
    for entity, labels in label_set1.items():
        for label, weight in labels.items():
            labels_w_from_first_set[label] = weight
    # get all labels & weights from all entities from entity set 2
    for entity, labels in label_set2.items():
        for label, weight in labels.items():
            labels_w_from_second_set[label] = weight
    print(labels_w_from_first_set)
    print("/n second_set /n")
    print(labels_w_from_second_set)
    dot_pr = dot_product(labels_w_from_first_set, labels_w_from_second_set)
    len_e1 = len(label_set1)
    len_e2 = len(label_set2)
    relatedness = (1 / (len_e1 * len_e2)) * dot_pr
    return relatedness

# formula 7
# def get_avg_weight_of_label_in_set(label_set: dict) -> float:
