from cloudtrade_zendesk import CloudTradeZendesk
import time

zendesk = CloudTradeZendesk('rumee.ahmed@cloud-trade.com')
response, total_count = zendesk.submit_intervention_tickets()

for count in range(total_count):
    response, total_count = zendesk.submit_intervention_tickets()
    remaining_api_calls = int(response.headers['X-Rate-Limit-Remaining'])
    print(remaining_api_calls)
    if remaining_api_calls < 250:
        print('Exceeding the API rate limit for this program')
        time.sleep(60)
