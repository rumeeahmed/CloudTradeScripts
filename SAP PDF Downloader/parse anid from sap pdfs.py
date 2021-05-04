import csv
import PyPDF2
from bs4 import BeautifulSoup
import os

file_names = []
with open('csvs/sap_files.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        file_names.append(row)

walk_dir = '/Users/rumeeahmed/Documents/Python-Projects/CloudTrade/SAP PDF Downloader/sap_reprocess'
for subdir, dirs, files in os.walk(walk_dir):
    for file in files:
        with open(f'sap_reprocess/{file}', 'rb') as pdf_file:

            try:
                # Open the PDF, get the last page extract the text and then create a soup object that parses xml.
                pdfReader = PyPDF2.PdfFileReader(pdf_file)
                pagehandle = pdfReader.getPage(-1)
                xml = pagehandle.extractText()
                soup = BeautifulSoup(xml, 'lxml')

                # Get the ANID from the xml, if none exists then populate variable with dummy string
                try:
                    buyer_anid = soup.find_all('extrinsic')[-1].get_text()
                except Exception:
                    buyer_anid = 'No Backing Data Found'

                # Split the directory name and the .pdf suffix from the pdf_files name attribute.
                file_namex = pdf_file.name.split('/')[1]
                file_name = file_namex.split('.pdf')[0]

            except Exception:
                buyer_anid = 'No Backing Data Found'

            # Check if the filename in the csv matches the file_name that is currently open then add the BuyerANID
            for index, name in enumerate(file_names):
                if name[0] == file_name:
                    file_names[index].append(buyer_anid)

# Create new CSV with the corresponding BuyerANID.
with open('csvs/sap_files_2.csv', 'w') as sap_file:
    csv_writer = csv.writer(sap_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Filename', 'URL', 'Buyer ANID'])

    for name in file_names:
        csv_writer.writerow(name)
