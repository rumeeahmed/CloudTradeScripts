# DiverseyPOCleaner
This script is designed to clean Diversey's PO feed. The file is supposed to be limited to a 15 column csv but due to
the way this is created it comes out as a file with 16 columns. Not only this but the commas in inside the text are not
escaped correctly this creating more columns than necessary.

This file will be executed on a daily basis on the `Diversey` user to clean their file. Then the existing Powershell
script will pull the new cleaned file to be uploaded to Gratabase.


---


## Usage
To use the script, an object of `DiverseyPOCleaner` must be instantiated with five parameters:
```python
directory_path = r'D:\FTP\Diversey\Prod\AribaPOLookup'
clean_write_path = r'D:\FTP\Diversey\Prod\AribaPOLookup\Cleaned Files'
unclean_write_path = r'D:\FTP\Diversey\Prod\AribaPOLookup\Rejections'
archive_path = r'D:\FTP\Diversey\Prod\AribaPOLookup\Archive'
row_length = 15

po = DiverseyPOCleaner(directory_path, clean_write_path, unclean_write_path, archive_path)
```
The `direcotry_path` represents where the original file is located.

The `clean_write_path` represents the location to write the new cleaned file.

The `unclean_write_path` represents the location to write the stripped out rows from the original feed.

The `archive_path` represents the location to the original po feed file to.

The `row_length` represents the number of expected rows to clean the po feed by. For example if the rows are supposed
to be 15 in length but due to extra commas the actual length of the rows are 17.

To execute the program use the following:
```python
po.execute()
```
