import csv
# mock data

country_data = [
    ["Country", "Capital", "Continent", "Leader", "Country_ISO_Code_2_Dig", "Country_ISO_Code_3_Dig", "Population", "Male_Height_AVG", "Female_Height_AVG", "Official_Language"],
    ["Germany", "Berlin", "Europe", "Olaf Scholz", "DE", "DEU", 81802257, 180.28, 166.18, "German"],
    ["China", "Peking", "Asia", "Xi Jinping", "CN", "CHN", 1330044000, 175.66, 163.46, "Chinese"],
    ["South Korea", "Seoul", "Asia", "Yoon Suk Yeol", "KR", "KOR", 48422644, 175.52, 163.23, "Korean"],
    ["France", "Paris", "Europe", "Emmanuel Macron", "FR", "FRA", 64768389, 178.60, 164.49, "French"],
    ["Ghana", "Accra", "Afrika", "Nana Akufo-Addo", "GH", "GHA", 24339838, 170.30, 158.86, "English"] 
]
# Define the name of the CSV file
csv_filename = "countries_database.csv"

# Create and write data to the CSV file
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(country_data)