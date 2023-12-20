import pandas as pd
import spacy


# extract entities from the first/second column
def extract_entities_from_table(input_table):
    try:
       table = pd.read_csv(input_table)
       for i in range(len(table.columns)):
            values = table.iloc[:, i]    # values of this column
            if 'id' not in table.columns[i].lower() and 'number' not in table.columns[i].lower():
                first_value = values.iloc[0]
                print(f"first value of the column : {first_value}")
                if not pd.isnull(first_value):
                    if not isinstance(first_value, (int, float)):
                        try:
                            pd.to_datetime(first_value)  # Check if the value can be converted to a date
                        except ValueError:
                            # If it raises a ValueError, it's neither int, float, nor date
                            return values.tolist()
            else:
            # Extract entities from the current column
                i += 1
                entities = table.iloc[:, i].tolist()
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
