import csv
import requests
import os
import PyPDF2
from bs4 import BeautifulSoup


class ANIDExtractor:
    def __init__(self, file_path: str, write_path: str):
        """
        Takes a csv and extracts its data, then downloads a bunch of pdfs, reads the attached xml, retrieves the
        supplier ANID from the xml and creates a csv file.
        :param file_path: the filepath of the csv.
        :param write_path: the write path of the csv containing supplier ANID's
        """
        self.file_path = file_path
        self.write_path = write_path

    def _process_csv(self):
        """
        Open the csv and extract the data.
        :return: list object containing all the rows in a csv.
        """
        self._data = []
        with open(f'{self.file_path}', 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                self._data.append(row)

    def _get_pdfs(self):
        """
        Make a get request on the URLs and download the pdf files.
        :return: pdf files.
        """
        for row in self._data:
            response = requests.get(row[-1])
            file = open(f'mapping_reprocess/{row[0]}.pdf', 'wb')
            file.write(response.content)
            file.close()

    def _parse_anid(self):
        """
        Open up the pdfs and parse the supplier anids from the xml backing data.
        :return: a list object containing the supplier anids
        """
        files = os.listdir('mapping_reprocess')
        self._supplier_anid = []
        for index, file in enumerate(files):
            with open(f'mapping_reprocess/{file}', 'rb') as pdf_file:
                try:
                    pdfReader = PyPDF2.PdfFileReader(pdf_file)
                    page_handle = pdfReader.getPage(-1)
                    xml = page_handle.extractText()
                    soup = BeautifulSoup(xml, 'lxml')
                    from_tag = soup.find('from')
                    supplier_anid = from_tag.find('identity').get_text()

                except Exception:
                    supplier_anid = 'No ANID Found'

                finally:
                    self._supplier_anid.append([supplier_anid])

    def _write_file(self):
        """
        Write the file containing the supplier anid
        :return: a csv file
        """
        with open(f'{self.write_path}/SAP Mapping Request Affected ANIDs.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            for anid in self._supplier_anid:
                csv_writer.writerow(anid)

    def execute(self):
        """
        Execute all the protected methods in one go.
        :return: a csv file
        """
        self._process_csv()
        self._get_pdfs()
        self._parse_anid()
        self._write_file()


file_path = 'SAP Mapping Requests c33dea08-3e63-4429-a67b-5f90132f9061.csv'
write_path = '/Users/rumeeahmed/Documents/CloudTradeScripts/SAP Mapping Request ANID Extractor'
anid = ANIDExtractor(file_path, write_path)
anid.execute()
