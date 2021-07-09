from cloudtrade_zendesk import CloudTradeZendesk
import shutil
import os

file_path = r'C:\Users\rumee.ahmed\Documents\Rules\Python\Mapping Requests'
move_path = ''
customer = 'Test'
pdfs = os.listdir(file_path)

for pdf in pdfs:
    if pdf.endswith('.pdf'):
        zendesk = CloudTradeZendesk('rumee.ahmed@cloud-trade.com')
        response = zendesk.send_mapping(customer, f'{file_path}\\{pdf}')
        shutil.move(f'{file_path}\\{pdf}', move_path)
        remaining_api_calls = int(response[1]['X-Rate-Limit-Remaining'])
        if remaining_api_calls < 200:
            print('Exceeding the API rate limit for this program')
            break
