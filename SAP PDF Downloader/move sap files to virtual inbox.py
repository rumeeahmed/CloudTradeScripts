import shutil
import os
import csv

file_names = []
with open('csvs/sap_files_2.csv') as sap_file:
    csv_reader = csv.reader(sap_file, delimiter=',')
    next(csv_reader)

    for row in csv_reader:
        file_names.append(row)

files_not_moved = []
for names in file_names:
    file_name = names[0] + '.pdf'
    url = names[1]
    buyer_anid = None
    if names[-1].startswith('AN'):
        buyer_anid = names[-1]

    if buyer_anid:
        path = '/Users/rumeeahmed/Documents/Python-Projects/CloudTrade/SAP PDF Downloader/Virtual Inbox'
        path = path.strip()

        if os.path.exists(f'{path}/{buyer_anid}'):
            shutil.copy(f'sap_reprocess/{file_name}', f'Virtual Inbox/{buyer_anid}')
        else:
            files_not_moved.append([file_name, url, buyer_anid])

with open('csvs/files_not_moved.csv', 'w') as files_unmoved:
    employee_writer = csv.writer(files_unmoved, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow(['Filename', 'URL', 'Buyer ANID'])

    for file in files_not_moved:
        employee_writer.writerow(file)
