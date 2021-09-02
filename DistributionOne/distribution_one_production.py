from csv_formatter import CSVModifier
import os

file_directory = r'C:\Users\rumee.ahmed\Documents\CloudTradeScripts\DistributionOne'
move_directory = r'C:\Users\rumee.ahmed\Documents\CloudTradeScripts\DistributionOne\processed_files'

files = os.listdir(file_directory)
csv_files = [file for file in files if file.endswith('.csv')]

if files:
    for file in csv_files:
        modifier = CSVModifier(fr'{file_directory}\{file}', move_directory)
        modifier.process_csv()
