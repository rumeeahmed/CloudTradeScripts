import requests
import csv

file_names = []
with open('csvs/sap_files.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        file_names.append(row)

for name in file_names:
    response = requests.get(name[1])
    file = open(f'sap_reprocess/{name[0]}.pdf', 'wb')
    file.write(response.content)
    file.close()
