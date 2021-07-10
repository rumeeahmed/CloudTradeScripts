from cloudtrade_zendesk import CloudTradeZendesk
import time

zendesk = CloudTradeZendesk('rumee.ahmed@cloud-trade.com')
response, total_count = zendesk.submit_intervention_tickets()

for count in range(total_count):
    response, total_count2 = zendesk.submit_intervention_tickets()
    remaining_api_calls = int(response.headers['X-Rate-Limit-Remaining'])
    time.sleep(2)
    if remaining_api_calls < 350:
        print('Exceeding the API rate limit for this program, waiting 30 seconds.')
        time.sleep(30)
    if total_count2 == 0:
        print('No more tickets to close')
        break
