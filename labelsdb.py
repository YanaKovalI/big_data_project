import json
import sqlite3


def init_database():
    connection = sqlite3.connect("labels.db")
    cursor = connection.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master")
    fetched = tables.fetchone()
    print(fetched)
    if fetched is None:
        create_table()
    connection.close()


def create_table():
    connection = sqlite3.connect("labels.db")
    cursor = connection.cursor()
    create_statement = """
        CREATE TABLE IF NOT EXISTS labels(
            "entity" text PRIMARY KEY NOT NULL,
            "labels" text
        );
    """
    cursor.execute(create_statement)
    connection.close()


def get_labels(entity):
    connection = sqlite3.connect("labels.db")
    cursor = connection.cursor()
    statement = """
        SELECT *
        FROM labels
        WHERE entity = \'{0}\';
    """.format(entity)
    res = cursor.execute(statement)
    labels = res.fetchone()
    if not labels:
        return None
    labels = json.loads(labels[1])
    print(labels)
    connection.close()
    return labels


def put_labels(entity, labels):
    connection = sqlite3.connect("labels.db")
    cursor = connection.cursor()
    labels = json.dumps(labels)
    data = (entity, labels)
    statement = """
        INSERT or IGNORE INTO labels VALUES(?, ?)
    """
    cursor.execute(statement, data)
    connection.commit()
    connection.close()
