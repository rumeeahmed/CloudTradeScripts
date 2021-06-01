# Zendesk Forwarder

The purpose of this script is to bulk submit multiple pdfs into Zendesk as opposed to bulk submitting emails 
as there are rate limits to the number of emails that can be sent from one email into the helpdesk per hour.

## Usage
This script is designed to send all files in a specified directory into Zendesk, when using this script ensure 
that the filepath only contains mappings for the same customer. This script only searches for PDF files so
any other file types will be ignored.

Insert the path for the directory that contains all the pdfs on line 96 in the `file_path` variable and the `customer`
variable.
```python
file_path = '/Users/rumeeahmed/Documents/Mapping Requests'
customer_name = 'Test'
```
One thing to note is that the rate limit for the endpoint is 400 per minute. To ensure that the limit is not used up 
the program will stop sending files to the API when the limit is below 200. So ensure that the number of pdf files in 
the directory does not exceed 200. If this does happen send the documents into the helpdesk in batches.