import pandas as pd
import spacy


# extract entities from the first/second column
def extract_entities_from_table(input_table):
    try:
        table = pd.read_csv(input_table)
        # Check if the first column is named 'id'
        if 'id' in table.columns[0].lower():
            # If it's an "id" column, return entities from the second column
            return table.iloc[:, 1].tolist()
        else:
            # Extract entities from the first column
            entities = table.iloc[:, 0].tolist()
            entities = cleanup_entitites(entities)
            return entities

    except Exception as e:
        print(str(e) + "at table " + str(input_table))


def cleanup_entitites(entities: list):
    new_entities = []
    for entity in entities:
        new_entity = entity.lower()
        new_entity = new_entity.title()
        new_entities.append(new_entity)
    return new_entities

# extract entities using nlp
def extract_entities_from_table_with_nlp(input_table):
    table = pd.read_csv(input_table)
    # Load the spaCy model 
    nlp = spacy.load("en_core_web_sm")

    entities = []

    # Iterate through the rows of the table
    for index, row in table.iterrows():
        # Process the text in each cell of the row
        for cell in row:
            # Apply spaCy NLP pipeline to extract entities
            doc = nlp(str(cell))
            # Extract entities from the document
            for ent in doc.ents:
                if ent.label_ != "CARDINAL":
                    entities.append(ent.text)
    return entities

# extracted_entities = extract_entities_from_table("contries_database.csv")
# extracted_entities_nlp = extract_entities_from_table_with_nlp("contries_database.scv") 

# print(extracted_entities)
