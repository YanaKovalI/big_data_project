import pandas as pd

# create mockdata
# tennis players 2  tables
table1 = pd.DataFrame({
    'Rank': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Surname': ['Nadal', 'Federer', 'Djonkovic', 'Murray', 'Soderling', 'Berdych', 'Ferrer', 'Roddick', 'Verdasco', 'Youzhny'] ,
     'Name' : ['Rafael','Roger', 'Novak', 'Andy', 'Robin', 'Tomas', 'David', 'Andy', 'Fernando', 'Mikhail'],
    'Points': [12.450, 9.145, 6.240, 5.760, 5.580, 3.955, 3.735, 3.665, 3.240, 2.920]
    })

table2 = pd.DataFrame({
    'Rank': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'Surname': ['Gill', 'Phau', 'Beck', 'Brands', 'Falla', 'Dimitrov', 'Bolelli', 'Devvarman', 'Darcis', 'Zeballos'] ,
     'Name' : ['Frederico','Bjorn', 'Karol', 'Daniel', 'Alejandro', 'Grigor', 'Simone', 'Somdev', 'Steve', 'Horacio'],
    'Points': [551, 551, 549, 541, 540, 536, 532, 526, 521, 517]
     } )



# dictionary to store the tables
dataset = {
    'Players1': table1,
    'Players2': table2
}
# just to see the data
print("Top 10 Players:")
print(dataset['Players1'])

print("\n 101-200 ranked players:")
print(dataset['Players2'])
