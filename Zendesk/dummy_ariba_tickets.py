from cloudtrade_zendesk import CloudTradeZendesk

zendesk = CloudTradeZendesk('rumee.ahmed@cloud-trade.com')
print(zendesk.submit_junk_ariba_tickets('subject:"Your Service Requests have been closed"'))
print(zendesk.submit_junk_ariba_tickets('subject:"Your Ariba Request was Unable to be Processed"'))