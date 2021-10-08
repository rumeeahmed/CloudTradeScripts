from cloudtrade_zendesk import CloudTradeZendesk
import shutil
import os
import time

username = 'ct6@cloud-trade.com'
file_path = r'C:\Users\rumee.ahmed\Downloads\files'
move_path = r'C:\Users\rumee.ahmed\Downloads\moved'
customer = 'Test'
files = os.listdir(file_path)

for file in files:
    if file.endswith('.zip'):
        zendesk = CloudTradeZendesk(username)
        response = zendesk.send_mapping(customer, f'{file_path}\\{file}')
        shutil.move(f'{file_path}\\{file}', move_path)
        remaining_api_calls = int(response.headers['X-Rate-Limit-Remaining'])
        if remaining_api_calls < 350:
            print('Exceeding the API rate limit for this program, waiting 30 seconds.')
            time.sleep(30)
