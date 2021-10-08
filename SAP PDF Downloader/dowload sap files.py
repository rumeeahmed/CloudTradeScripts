import requests
import csv
import time

file_names = []
with open(r'C:\Users\rumee.ahmed\Downloads\Bucks Resubmit without Duplicates.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        file_names.append(row)


for name in file_names:
    time.sleep(1)
    try:
        response = requests.get(name[-1])
    except:
        response = requests.get(name[-2])
    file = open(f'C:\\Users\\rumee.ahmed\\Downloads\\bucks no duplicates\\{name[0]}.pdf', 'wb')
    file.write(response.content)
    file.close()
