import pandas as pd
import spacy

input_table = pd.read_csv("countries_database.csv")

#extract entities from the first/second column
def extract_entities_from_table(table):
    # Check if the first column is named 'id'
    if 'id' in table.columns[0].lower():
        # If it's an "id" column, return entities from the second column
        return table.iloc[:, 1].tolist()
    else:
        # Extract entities from the first column
        entities = table.iloc[:, 0].tolist()
        return entities

#extract entities using nlp
def extract_entities_from_table_with_nlp(table):
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


extracted_entities = extract_entities_from_table(input_table)
extracted_entities_nlp = extract_entities_from_table_with_nlp(input_table) 

# print(extracted_entities)

