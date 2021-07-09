from zendesk_forwarder import ZendeskForwarder

zendesk = ZendeskForwarder('rumee.ahmed@cloud-trade.com')
zendesk.submit_junk_ariba_tickets('subject "Your Service Requests have been closed"')
zendesk.submit_junk_ariba_tickets('subject "Your Ariba Request was Unable to be Processed"')
