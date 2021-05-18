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
One thing to note is that the rate limit for the endpoint is 400 per second, so ensure that the number of pdf 
files in the directory does not exceed 400. Whilst this is highly unlikely the below loop can be modified to slow
down the POST requests to the API after every submission or after a certain number of submissions using the `time`
module.
```python
import time
for pdf in pdfs:
    if pdf.endswith('.pdf'):
        zendesk = ZendeskForwarder(customer, f'{file_path}\\{pdf}')
        zendesk.send()
        time.sleep(1)
```