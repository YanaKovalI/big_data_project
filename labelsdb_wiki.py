import json
import sqlite3

def init_database():
    connection = sqlite3.connect("wikidata_labels.db")
    cursor = connection.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master")
    fetched = tables.fetchall()
    if fetched is None or not fetched:
        create_table()
    connection.close()


def create_table():
    connection = sqlite3.connect("wikidata_labels.db")
    cursor = connection.cursor()
    create_statement_entity_label = """
        CREATE TABLE IF NOT EXISTS labels(
            "entity" text NOT NULL,
            "label" text NOT NULL,
            PRIMARY KEY (entity, label)
            FOREIGN KEY (label) REFERENCES weights(label)
        );
    """
    create_statement_entity_weights = """
        CREATE TABLE IF NOT EXISTS weights(
            "label" text PRIMARY KEY NOT NULL,
            "weight" float
        );
    """
    create_statement_no_labels = """
        CREATE TABLE IF NOT EXISTS no_labels(
            "entity" text PRIMARY KEY NOT NULL
        );
    """
    cursor.execute(create_statement_entity_label)
    cursor.execute(create_statement_entity_weights)
    cursor.execute(create_statement_no_labels)
    connection.close()


def get_weighted_labels(entity):
    connection = sqlite3.connect("wikidata_labels.db")
    cursor = connection.cursor()
    statement = """
        SELECT
            l.label,
            w.weight
        FROM labels l
            INNER JOIN weights w ON w.label = l.label 
        WHERE entity = ?;
    """
    res = cursor.execute(statement, (entity,))
    labels = res.fetchall()
    connection.close()
    if not labels:
        if is_entity_labelless(entity):
            return dict()
        else:
            return None
    weighted_labels = dict(labels)
    return weighted_labels


def is_entity_labelless(entity):
    connection = sqlite3.connect("wikidata_labels.db")
    cursor = connection.cursor()
    statement = """
        SELECT entity
        FROM no_labels
        WHERE entity = ?
    """
    res = cursor.execute(statement, (entity,))
    is_labellles = res.fetchone()
    connection.close()
    if not is_labellles:
        return False
    return True


def get_weight(label):
    connection = sqlite3.connect("wikidata_labels.db")
    cursor = connection.cursor()
    statement = """
        SELECT
            weight
        FROM
            weights
        WHERE
            label = ?;
    """
    res = cursor.execute(statement, (label,))
    weight = res.fetchone()
    connection.close()
    if not weight:
        return None
    return weight[0]


def put_weighted_labels(entity, weighted_labels):
    put_weights(weighted_labels)
    put_labels(entity, weighted_labels.keys())


def put_weights(weighted_labels: dict):
    connection = sqlite3.connect("wikidata_labels.db")
    cursor = connection.cursor()
    data = weighted_labels.items()
    statement = """
        INSERT or IGNORE INTO weights VALUES(?, ?)
    """
    for tuple in data:
        try:
            cursor.execute(statement, tuple)
        except Exception as e:
            print(e)
    connection.commit()
    connection.close()


def put_labels(entity, weighted_label):
    connection = sqlite3.connect("wikidata_labels.db")
    cursor = connection.cursor()
    statement = """
        INSERT or IGNORE INTO labels VALUES(?, ?)
    """
    for label in weighted_label:
        data = (entity, label)
        try:
            cursor.execute(statement, data)
        except Exception as e:
            print(e)
    connection.commit()
    connection.close()


def put_labelless_entity(entity):
    connection = sqlite3.connect("wikidata_labels.db")
    cursor = connection.cursor()
    statement = """
        INSERT or IGNORE INTO no_labels VALUES(?)
    """
    try:
        cursor.execute(statement, (entity,))
        connection.commit()
    except Exception as e:
        print(e)
    connection.close()
