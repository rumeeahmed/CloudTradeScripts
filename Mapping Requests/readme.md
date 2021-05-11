#Zendesk Forwarder

The purpose of this script is to bulk submit multiple pdfs into Zendesk as opposed to bulk submitting emails 
as there are limits to this.

##Usage
This script is designed to send all files in a specified directory into Zendesk, when using this script ensure 
that the filepath only contains mappings for the same customer. This script only searches for PDF files so
any other file types will be ignored.

Insert the path for the directory that contains all the pdfs on line 96 in the `file_path` variable.
```python
file_path = '/Users/rumeeahmed/Documents/Mapping Requests'
```
Then change the first parameter in the `ZendeskForwarder` class on line 101 as the customer name.
```python
zendesk = ZendeskForwarder('Customer Name', f'{file_path}/{pdf}')
```
The limit is 400 requests to the endpoint per second so ensure that the mappings do not exceed 400.