# Zendesk

The purpose of the `CloudTradeZendesk` program is to work with CloudTrade's Zendesk API and automate various
functionality.

One thing to note that the rate limit for the endpoint is 400. To ensure that the limit is not used up this program
adds a 2 second time delay per request and a 30 second time delay when the remaining Api calls fall below 350. Ensure
that the program is not accidentally closed before it finishes execution.

## Usage

There are various different functionalty the `CloudTradeZendesk` object provides. Listed below are the functionality
it currently supports:

### Bulk Submitting Mapping Requests

This script is designed to bulk submit new pdf mapping requests into Zendesk. The way this works is a directory with
all the mappings must be specified as well as an empty directory to move the completed mappings to, it only searches
for PDF files so any other filetype will be ignored.

Change the `file_path` variable to the filepath where all the pdfs reside, then change the `move_path` variable to
the path that the pdfs should be moved to when it has been posted into Zendesk and finally change the `customer`
variable to ensure that the subject reflects which customer the mapping is for.

```python
username = 'ct6@cloud-trade.com'
file_path = r'C:\Users\rumee.ahmed\Documents\CloudTradeScripts\Mapping Requests\files'
move_path = r'C:\Users\rumee.ahmed\Documents\CloudTradeScripts\Mapping Requests\moved_files'
customer = 'Test'
```

### Closing Monthly Time Tracking Tickets

This script will also close any tickets that has the tag `monthly_time_tracking` that have been created since the
`1st` of the current month. It is designed to run on the last day of every month.

First instantiate the `CloudTradeZendesk` object that only takes in one parameter, which is the username. For this
feature the username needs to be an agent within CloudTrade, so using a staff member who is an agent on Zendesk is 
acceptable. The `submit_monthly_tickets` method will handle the HTTP request that searches for and submits monthly
tickets.

```python
zendesk = CloudTradeZendesk('rumee.ahmed@cloud-trade.com')
zendesk.submit_monthly_tickets()
```

**Note that the all the mandatory fields i.e., Channel Partner, `Customer`, `Ticket Type` and `Chargeable/Non-Chargeable`
must be filled out beforehand. Any tickets without these parameters will not be closed.**