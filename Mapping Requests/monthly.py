from zendesk_forwarder import ZendeskForwarder

zendesk = ZendeskForwarder('customer', f'hello', 'h')
monthly = zendesk.get_ticket_fields()
print(monthly)
