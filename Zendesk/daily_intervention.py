from cloudtrade_zendesk import CloudTradeZendesk
import time

zendesk = CloudTradeZendesk('rumee.ahmed@cloud-trade.com')
response, total_count = zendesk.submit_intervention_tickets()
print(total_count)

calls = total_count/100
for count in range(round(calls)):
    response, total_count = zendesk.submit_intervention_tickets()
    remaining_api_calls = int(response.headers['X-Rate-Limit-Remaining'])
    time.sleep(2)
    print(remaining_api_calls)
    if remaining_api_calls < 350:
        print('Exceeding the API rate limit for this program, waiting 30 seconds.')
        time.sleep(30)
