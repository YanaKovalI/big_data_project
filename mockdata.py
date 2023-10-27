import pandas as pd

#  mockdata
# tennis players 2  tables
input_table1 = pd.DataFrame({
    'Rank': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
     'Name': ['Nadal Rafael', 'Federer Roger', 'Djonkovic Novak', 'Murray Andy', 'Soderling Robin', 'Berdych Tomas', 'Ferrer David', 'Roddick Andy', 'Verdasco Fernando', 'Youzhny Mikhail'],
    'Points': [12.450, 9.145, 6.240, 5.760, 5.580, 3.955, 3.735, 3.665, 3.240, 2.920]
    })

input_table2 = pd.DataFrame({
    'Rank': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'Name': ['Gill Frederico', 'Phau Bjorn', 'Beck Karol', 'Brands Daniel', 'Falla Alejandro', 'Dimitrov Grigor', 'Bolelli Simone', 'Devvarman Somdev', 'Darcis Steve', 'Zeballos Horacio'],
    'Points': [551, 551, 549, 541, 540, 536, 532, 526, 521, 517]
     } )

# dictionary to store the tables
dataset = {
    'Players1': input_table1,
    'Players2': input_table2
}
# just to see the data
print("Top 10 Players:")
print(dataset['Players1'])

print("\n 101-200 ranked players:")
print(dataset['Players2'])

# Mock WikiData
wikidata_table1 = pd.DataFrame({
    'Entity' : ['Nadal Rafael', 'Federer Roger'],
    'Labels' : [['person','tennis_player', 'sportsmen', 'animal'], ['person', 'tennis_player', 'doctor']] ,
    'Weight' : [[1,0.98, 0.8, 0.1], [1,0.98,0.5]]
})
wikidataset = {
    'Wikidata_table' : wikidata_table1
}
print(wikidataset['Wikidata_table'].head())