from zendesk_forwarder import ZendeskForwarder

zendesk = ZendeskForwarder('rumee.ahmed@cloud-trade.com')
monthly = zendesk.submit_junk_ariba_tickets('Your Service Requests have been closed')
# zendesk.submit_junk_ariba_tickets('Your Ariba Request was Unable to be Processed')
print(monthly)
