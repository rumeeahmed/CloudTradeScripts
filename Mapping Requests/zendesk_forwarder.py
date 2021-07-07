from datetime import datetime
import requests
import base64
import json
import os


class ZendeskForwarder:
    """
    Object that creates a bulk Zendesk tickets.
    """

    base_url = 'https://cloudtrade.zendesk.com/api/v2'
    request_url = f'{base_url}/requests'
    uploads_url = f'{base_url}/uploads'
    search_url = f'{base_url}/search.json?'
    tickets_url = f'{base_url}/tickets/update_many.json?'

    username = 'rumee.ahmed@cloud-trade.com'
    token = ''

    def __init__(self, customer: str, filepath: str):
        self.customer = customer
        self.filepath = filepath
        self._encode_authentication_details()
        self._process_headers()
        self._prepare_data()

    def _encode_authentication_details(self):
        """
        Create a base64 encoded string out of the email and token parameters for the POST request. Convert the string
        into bytes, encode into a base64 encoded byte-string and then decode said byte-string to retrieve the string
        value of the email and token.
        :return: base64 encoded string.
        """
        params_bytes = f'{self.username}/token:{self.token}'.encode('ascii')
        params_b64 = base64.b64encode(params_bytes)
        bs4_string = params_b64.decode('ascii')
        self._encoded_auth_params = bs4_string

    def _process_headers(self):
        """
        Prepare the headers to be POSTED into the URL.
        :return: headers dict object
        """
        headers = {
            'authorization': f'Basic {self._encoded_auth_params}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        self._headers = headers

    def _prepare_data(self):
        """
        Prepare the data for the zendesk ticket.
        :return: data dict object
        """
        data = {
            'request': {
                "requester": {
                    "email": "no-reply@cloutrade-zendesk.com",
                    'name': 'Noreply',
                },
                "subject": f"New {self.customer} Mapping",
                "comment": {
                    "body": "Please see attached file for mapping"
                }
            }
        }
        self._data = data

    def _send_attachment(self) -> str:
        """
        Post the attachment first prior to ticket creation to obtain a attachment token to be link the attachment and
        ticket together in Zendesk.
        :return: attachment token
        """
        self._headers['Content-Type'] = 'application/pdf'
        self._headers['Accept'] = 'application/pdf'
        files = {'file': open(self.filepath, 'rb')}
        filename = os.path.basename(self.filepath)
        response = requests.post(f'{self.uploads_url}?filename={filename}', headers=self._headers, files=files)
        response.raise_for_status()
        content = response.json()
        return content['upload']['token']

    def send(self) -> tuple:
        """
        Make a POST request to the endpoint and create the ticket.
        :return: json API response object.
        """
        attachment_token = self._send_attachment()
        self._data['request']['comment']['uploads'] = [attachment_token]
        self._headers['Content-Type'] = 'application/json'
        self._headers['Accept'] = 'application/json'
        payload = json.dumps(self._data)
        response = requests.post(self.request_url, headers=self._headers, data=payload)
        response.raise_for_status()
        return response.json(), response.headers

    def _get_tickets(self, search_term: str) -> dict:
        """
        Make a get request on the search api to search for a specific ticket.
        :param search_term: The search term or parameters to use to narrow down or filter the search by.
        :return: A dictionary object containing all the results.
        """
        self._headers['Content-Type'] = 'application/json'
        self._headers['Accept'] = 'application/json'
        response = requests.get(f'{self.search_url}query={search_term}', headers=self._headers)
        response.raise_for_status()
        return response.json()

    def get_monthly_tickets(self) -> list:
        """
        Get the ticket id's for the monthly time tracking tickets.
        :return: A list object containing all the ticket id's.
        """
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')

        tickets = self._get_tickets(f'tags:monthly_time_tracking created>={year}-{month}-01 type:ticket status>solved')
        ticket_ids = [str(ticket['id']) for ticket in tickets['results']]
        return ticket_ids

    def bulk_submit_tickets(self) -> dict:
        """
        Bulk submit the tickets.
        :return: A dictionary object containing the response message.
        """
        ticket_ids = self.get_monthly_tickets()

        if ticket_ids:
            params = ','.join(ticket_ids)

            data = {'tickets': []}
            for ticket in ticket_ids:
                data['tickets'].append({'id': int(ticket), 'status': 'solved'})
            data = json.dumps(data)

            response = requests.put(f'{self.tickets_url}', headers=self._headers, params=params, data=data)
            response.raise_for_status()
            return response.json()
        else:
            print("No ticket ID's were found")
