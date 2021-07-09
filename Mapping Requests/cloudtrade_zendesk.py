from datetime import datetime
import requests
import base64
import json
import os


class CloudTradeZendesk:
    """
    Object that works with CloudTrade's Zendesk Api.
    """

    base_url = 'https://cloudtrade.zendesk.com/api/v2'
    request_url = f'{base_url}/requests'
    uploads_url = f'{base_url}/uploads'
    search_url = f'{base_url}/search.json?'
    tickets_url = f'{base_url}/tickets/update_many.json?'

    token = os.environ.get('DISCORD_KEY')

    def __init__(self, username: str):
        """

        :param username: a string value that represents the email username to use.
        """
        self.username = username
        self._encode_authentication_details()
        self._process_headers()

    def _encode_authentication_details(self):
        """
        Create a base64 encoded string out of the email and token parameters for the POST request. Convert the string
        into bytes, encode into a base64 encoded byte-string and then decode said byte-string to retrieve the string
        value of the email and token.
        :return: base64 encoded string of the authentication parameters required for communicating with the Zendesk Api.
        """
        params_bytes = f'{self.username}/token:{self.token}'.encode('ascii')
        params_b64 = base64.b64encode(params_bytes)
        bs4_string = params_b64.decode('ascii')
        self._encoded_auth_params = bs4_string

    def _process_headers(self):
        """
        Prepare the headers to be used with a request to the URL.
        :return: a dictionary object that represents the HTTP headers.
        """
        headers = {
            'authorization': f'Basic {self._encoded_auth_params}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        self._headers = headers

    def _prepare_data(self, customer: str):
        """
        Prepare the data for the zendesk ticket.
        :return: a dictionary object that represents a new ticket that is compatible with Zendesk's Api
        """
        data = {
            'request': {
                "requester": {
                    "email": "no-reply@cloutrade-zendesk.com",
                    'name': 'Noreply',
                },
                "subject": f"New {customer} Mapping",
                "comment": {
                    "body": "Please see attached file for mapping"
                }
            }
        }
        self._data = data

    def _send_attachment(self, filepath: str) -> str:
        """
        Post the attachment first prior to ticket creation to obtain a attachment token to be link the attachment and
        ticket together in Zendesk.
        :return: attachment token.
        """
        self._headers['Content-Type'] = 'application/pdf'
        self._headers['Accept'] = 'application/pdf'
        files = {'file': open(filepath, 'rb')}
        filename = os.path.basename(filepath)
        response = requests.post(f'{self.uploads_url}?filename={filename}', headers=self._headers, files=files)
        response.raise_for_status()
        content = response.json()
        return content['upload']['token']

    def send_mapping(self, customer: str, filepath: str) -> tuple:
        """
        Make a POST request to the endpoint and create the ticket.
        :return: json API response object.
        """
        attachment_token = self._send_attachment(filepath)
        self._prepare_data(customer)
        self._data['request']['comment']['uploads'] = [attachment_token]
        self._headers['Content-Type'] = 'application/json'
        self._headers['Accept'] = 'application/json'
        payload = json.dumps(self._data)
        response = requests.post(self.request_url, headers=self._headers, data=payload)
        response.raise_for_status()
        return response.json(), response.headers

    @staticmethod
    def _get_now() -> tuple:
        """
        Get the current date time in separate values to use for querying the search API.
        :return: a tuple containing the year, month and day in integer values.
        """
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')
        return year, month, day

    @staticmethod
    def _process_tickets(tickets: dict) -> list:
        """
        Process the JSON returned from the API and return a list of ticket ID's.
        :param tickets: the ticket JSON returned from the search API.
        :return: A list of all the ticket ID's searched for.
        """
        ticket_ids = [str(ticket['id']) for ticket in tickets['results']]
        return ticket_ids

    def _get_tickets(self, search_term: str) -> dict:
        """
        Make a get request on the search api to search for a specific ticket.
        :param search_term: The search term or parameters to use to narrow down or filter the search by.
        :return: A dictionary object containing all the search results.
        """
        self._headers['Content-Type'] = 'application/json'
        self._headers['Accept'] = 'application/json'
        response = requests.get(f'{self.search_url}query={search_term}', headers=self._headers)
        response.raise_for_status()
        return response.json()

    def submit_monthly_tickets(self):
        """
        Perform a search on the search api and submit any ticket created since the 1st of the current month with the tag
        `monthly_time_tracking`.
        :return: None.
        """
        year, month, day = self._get_now()
        tickets = self._get_tickets(f'tags:monthly_time_tracking created>={year}-{month}-01 type:ticket status<solved')
        ticket_ids = self._process_tickets(tickets)

        data = {'tickets': []}
        for ticket in ticket_ids:
            data['tickets'].append({'id': int(ticket), 'status': 'solved'})

        return self.bulk_submit_tickets(ticket_ids, data)

    def submit_junk_ariba_tickets(self, subject: str):
        """
        Perform a search on the search api for junk Ariba tickets created on the current day and then submit them.
        :param subject: a string value that represents the search term to perform on the Api.
        :return: a dictionary object that contains the response data.
        """
        year, month, day = self._get_now()
        tickets = self._get_tickets(f'{subject} created>={year}-{month}-{day} type:ticket status<solved')

        ticket_ids = self._process_tickets(tickets)
        data = self._create_solved_tickets_json_body(ticket_ids)
        custom_fields = [
            {'id': 360010677313, "value": "sap"},
            {'id': 360014557454, "value": "ariba_network"},
            {'id': 360014549894, "value": "non-chargeable"},
            {"id": 24037427, "value": "rules_writing_support"}
        ]
        for ticket in data['tickets']:
            ticket['custom_fields'] = custom_fields

        return self.bulk_submit_tickets(ticket_ids, data)

    @staticmethod
    def _create_solved_tickets_json_body(ticket_ids: list) -> dict:
        """
        Take a list of ticket ids and create a dictionary object that is compliant with the API which will be then used
        to bulk update tickets.
        :param ticket_ids: A list object containing the ticket IDs to bulk update.
        :return: A dictionary object representing the tickets to update that is in the format required for the Zendesk
        Api.
        """
        data = {'tickets': []}
        for ticket in ticket_ids:
            data['tickets'].append({'id': int(ticket), 'status': 'solved'})
        return data

    def bulk_submit_tickets(self, ticket_ids: list, data: dict) -> dict:
        """
        Take a list of ticket ID's and bulk submit all of the.
        :param ticket_ids: a list object containing string values representing the ticket ID to update.
        :param data: a dictionary object to post as a json file which include the details to update the ticket by.
        :return: a dictionary object that contains the response data.
        """
        if ticket_ids:
            params = ','.join(ticket_ids)
            data = json.dumps(data)
            response = requests.put(f'{self.tickets_url}', headers=self._headers, params=params, data=data)
            response.raise_for_status()
            return response.json()
        else:
            print("No ticket ID's were found")

    def get_ticket_fields(self):
        """
        This method will return all the possible ticket fields that are available in in the CloudTrade Zendesk API.
        :return: a dictionary object that contains the response data.
        """
        response = requests.get(f'https://cloudtrade.zendesk.com/api/v2/ticket_fields', headers=self._headers)
        response.raise_for_status()
        return response.json()

