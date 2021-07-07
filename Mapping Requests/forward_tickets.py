from zendesk_forwarder import ZendeskForwarder
import os

file_path = r'C:\Users\rumee.ahmed\Documents\Rules\Python\Mapping Requests'
customer = 'Test'
pdfs = os.listdir(file_path)

for pdf in pdfs:
    if pdf.endswith('.pdf'):
        zendesk = ZendeskForwarder(customer, f'{file_path}\\{pdf}')
        response = zendesk.send()
        remaining_api_calls = int(response[1]['X-Rate-Limit-Remaining'])
        if remaining_api_calls < 200:
            print('Exceeding the API rate limit for this program')
            break
