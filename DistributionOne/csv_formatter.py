from datetime import datetime
import csv
import os


class CSVModifier:
    """
    Object that handles Distribution One's CSV output.
    """
    def __init__(self, file_directory: str, move_path: str):
        self.file_directory = file_directory
        self.move_path = move_path
        self.lines = []

    def _find_file(self) -> str:
        """
        Find the csv file in the provided directory.
        :return: a string object with the name of the found csv file.
        """
        files = os.listdir(self.file_directory)
        csv_file = ''
        for file in files:
            if file.endswith('.csv'):
                csv_file = file
        return csv_file

    def process_csv(self) -> None:
        """
        Open the csv file and extract all its lines.
        :return: None
        """
        csv_file = self._find_file()
        if csv_file:
            with open(f'{self.file_directory}\\{csv_file}') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='|')
                for line in csv_reader:
                    self.lines.append(line)

        self._write_csv()

    def _write_csv(self) -> None:
        """
        Write a csv file with extracted values in `self.lines`.
        :return: None
        """
        now = datetime.now().strftime('%Y-%m-%d')
        with open(f'{self.move_path}\\distribution_one_{now}.csv', 'w', newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='|')
            for line in self.lines:
                csv_writer.writerow(line)


csv_modifier = CSVModifier(
    r'C:\Users\rumee.ahmed\Documents\CloudTradeScripts\DistributionOne',
    r'C:\Users\rumee.ahmed\Documents\CloudTradeScripts\DistributionOne'
)
csv_modifier.process_csv()
