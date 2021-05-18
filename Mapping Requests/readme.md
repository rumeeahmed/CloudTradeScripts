#Zendesk Forwarder

The purpose of this script is to bulk submit multiple pdfs into Zendesk as opposed to bulk submitting emails 
as there are limits to this.
-----

##Usage
This script is designed to send all files in a specified directory into Zendesk, when using this script ensure 
that the filepath only contains mappings for the same customer. This script only searches for PDF files so
any other file types will be ignored. This should also be used on a per-customer basis as it will assume all
the files in the specified directory belongs to the same customer.

Insert the path for the directory that contains all the pdfs on line 96 in the `file_path` variable.
```python
file_path = '/Users/rumeeahmed/Documents/Mapping Requests'
```

Then change the first parameter in the `ZendeskForwarder` class on line 101 as the customer name, this will
then be in the subject line of the ticket in Zendesk.

```python
zendesk = ZendeskForwarder('Customer Name', f'{file_path}/{pdf}')
```

One thing to note is that the rate limit for the endpoint is 400 per second so ensure that the number of pdf
files in the directory do not exceed 400. Whilst this is highly unlikely the below loop can be modified to
slow down POST requests to the API after every submission or after a certain number of submissions using the
`time` module.
```python
import time
for pdf in pdfs:
    if pdf.endswith('.pdf'):
        zendesk = ZendeskForwarder('Test', f'{file_path}/{pdf}')
        zendesk.send()
        time.sleep(1)
```