import os
import csv
import shutil


class CSVModifier:
    """
    Object that handles Distribution One's CSV output.
    """
    def __init__(self, filepath: str, move_path: str, archive_path: str):
        """

        :param filepath: the file name of the csv.
        :param move_path: the directory to write the new csv file to.
        :param archive_path: the directory to move the original csv file to.
        """
        self.filepath = filepath
        self.move_path = move_path
        self.archive_path = archive_path
        self.lines = []

    def process_csv(self) -> None:
        """
        Open the csv file and extract all its lines.
        :return: None
        """
        with open(f'{self.filepath}') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            for line in csv_reader:
                self.lines.append(line)

        self._write_csv()
        shutil.move(self.filepath, self.archive_path)

    def _write_csv(self) -> None:
        """
        Write a csv file with extracted values in `self.lines`.
        :return: None
        """
        name = os.path.basename(self.filepath)
        with open(f'{self.move_path}\\{name}', 'w', newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='|')
            for line in self.lines:
                csv_writer.writerow(line)
