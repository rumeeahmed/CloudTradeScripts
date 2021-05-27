import requests
import base64
import json
import os


class ZendeskForwarder:
    """
    Object that creates a bulk Zendesk tickets.
    """

    request_url = 'https://cloudtrade.zendesk.com/api/v2/requests'
    uploads_url = 'https://cloudtrade.zendesk.com/api/v2/uploads'
    username = 'noreply@cloud-trade.net'
    token = os.environ.get('ZENDESK_KEY')

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
        :return: base64 encoded string
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

    def _send_attachment(self):
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
        content = response.json()
        return content['upload']['token']

    def send(self):
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
        return response.json()


file_path = '/Users/rumeeahmed/Documents/CloudTradeScripts/Mapping Requests'
customer = 'Test'
pdfs = os.listdir(file_path)

for pdf in pdfs:
    if pdf.endswith('.pdf'):
        zendesk = ZendeskForwarder(customer, f'{file_path}/{pdf}')
        zendesk.send()
