from zendesk_forwarder import ZendeskForwarder

zendesk = ZendeskForwarder('customer', f'hello')
zendesk.bulk_submit_tickets()
