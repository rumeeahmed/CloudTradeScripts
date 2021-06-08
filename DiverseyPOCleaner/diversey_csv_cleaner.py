import csv
import os
import shutil
from datetime import datetime


class DiverseyPOCleaner:
    """
    Object that cleans Diversey's PO feed.
    """
    def __init__(
            self, directory_path: str,
            clean_write_path: str,
            unclean_write_path: str,
            archive_path: str,
            row_length: int
    ):
        """
        :param directory_path: The directory that contains the csv.
        :param clean_write_path: The directory to write the cleaned csv file to.
        :param unclean_write_path: The directory to write the uncleaned csv file to.
        :param archive_path: The directory to move the original file to.
        :param archive_path: The number of expected rows to clean the file by.
        """

        self.directory_path = directory_path
        self.clean_write_path = clean_write_path
        self.unclean_write_path = unclean_write_path
        self.archive_path = archive_path
        self.row_length = row_length

    def _clean(self):
        """
        Process the original csv and separate rows that are equal to 15 and any row not equal to 15 in their own class
        variables.
        :return: a list object with clean rows equal to 15 items per row and another list object containing any
        original rows where the items are greater than 15.
        """

        self._rows_cleaned = []
        self._rows_not_cleaned = []

        files = os.listdir(self.directory_path)
        csvs = [file for file in files if file.endswith('.csv')]
        self._original_file_name = csvs[-1]

        with open(f'{self.directory_path}/{self._original_file_name}', 'r', encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

            for row in csv_reader:
                while '' in row:
                    row.remove('')

                if len(row) == int(row_length):
                    self._rows_cleaned.append(row)
                else:
                    self._rows_not_cleaned.append(row)

    def _write_cleaned_csv(self):
        """
        Write a CSV using the cleaned data.
        :return: A cleaned CSV for gratabase to ingest.
        """

        self._now = datetime.now().strftime('%d %m %Y %H %M %S')
        filename = f"{self._original_file_name.strip('.csv')}_cleaned_{self._now}.csv"

        with open(f'{self.clean_write_path}/{filename}', 'w', newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            for row in self._rows_cleaned:
                csv_writer.writerow(row)

    def _write_uncleaned_csv(self):
        """
        Write the rows that were greater than 15 and cannot be ingested by Gratabase.
        :return: A csv containing the rows that need to be removed from the PO feed.
        """

        file_name = f"{self._original_file_name.strip('.csv')}_uncleaned_{self._now}.csv"
        with open(f'{self.unclean_write_path}/{file_name}', 'w', newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            for row in self._rows_not_cleaned:
                csv_writer.writerow(row)

    def _move_original_file(self):
        """
        Move the original file to an archived location
        :return: None
        """
        try:
            shutil.move(f'{self.directory_path}/{self._original_file_name}', self.archive_path)
        except shutil.Error:
            shutil.move(
                f'{self.directory_path}/{self._original_file_name}'
                , f'{self.archive_path}/prexisting {self._now}{self._original_file_name}'
            )
        
    def process_csv(self):
        """
        Execute all the above commands in one go.
        :return: Two cleaned csv files.
        """
        self._clean()
        self._write_cleaned_csv()
        self._write_uncleaned_csv()
        self._move_original_file()


directory_path = r'/Users/rumeeahmed/Documents/CloudTradeScripts/DiverseyPOCleaner'
clean_write_path = r'/Users/rumeeahmed/Documents/CloudTradeScripts/DiverseyPOCleaner/cleaned'
unclean_write_path = r'/Users/rumeeahmed/Documents/CloudTradeScripts/DiverseyPOCleaner/unclean'
archive_path = r'/Users/rumeeahmed/Documents/CloudTradeScripts/DiverseyPOCleaner/archive'
row_length = 15

po = DiverseyPOCleaner(directory_path, clean_write_path, unclean_write_path, archive_path, row_length)
po.process_csv()

