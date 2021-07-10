from cloudtrade_zendesk import CloudTradeZendesk
import shutil
import os
import time

username = 'ct6@cloud-trade.com'
file_path = r'C:\Users\rumee.ahmed\Documents\CloudTradeScripts\Mapping Requests\files'
move_path = r'C:\Users\rumee.ahmed\Documents\CloudTradeScripts\Mapping Requests\moved_files'
customer = 'Test'
pdfs = os.listdir(file_path)

for pdf in pdfs:
    if pdf.endswith('.pdf'):
        zendesk = CloudTradeZendesk(username)
        response = zendesk.send_mapping(customer, f'{file_path}\\{pdf}')
        shutil.move(f'{file_path}\\{pdf}', move_path)
        remaining_api_calls = int(response.headers['X-Rate-Limit-Remaining'])
        if remaining_api_calls < 350:
            print('Exceeding the API rate limit for this program, waiting 30 seconds.')
            time.sleep(30)
