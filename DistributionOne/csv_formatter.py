from datetime import datetime
import csv


class CSVModifier:
    """
    Object that handles Distribution One's CSV output.
    """
    def __init__(self, filepath: str, move_path: str):
        """

        :param filepath: the file name of the csv.
        :param move_path: the directory to write the new csv file in.
        """
        self.filepath = filepath
        self.move_path = move_path
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

    def _write_csv(self) -> None:
        """
        Write a csv file with extracted values in `self.lines`.
        :return: None
        """
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')
        with open(f'{self.move_path}\\distribution_one_{now}.csv', 'w', newline='', encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='|')
            for line in self.lines:
                csv_writer.writerow(line)
