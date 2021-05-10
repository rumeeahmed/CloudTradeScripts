import smtplib
from email.message import EmailMessage
import requests


class MappingRequest:
    """
    Represents a Mapping Request object.
    """
    from_email = 'noreply@cloud-trade.net'

    def __init__(self, to_email: str, customer: str, pdf_filepath: str):
        self.to_email = to_email
        self.customer = customer
        self.pdf_filepath = pdf_filepath

    def _build_message(self):
        """
        Build the message object.
        :return: A message object.
        """
        msg = EmailMessage()
        msg.set_content('Please see attached examples(s) for mapping.')
        msg['Subject'] = f'{self.customer} Mapping Request'
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        return msg

    def send_email(self):
        msg = self._build_message()
        server = smtplib.SMTP('email-smtp.us-east-1.amazonaws.com', 587)
        server.starttls()
        server.login('ct6@cloud-trade.com', 'V$wnu@ryAJjW8++k')
        server.send_message(msg, self.from_email, self.to_email)
        server.quit()


mapping_request = MappingRequest(
    'RumeeAhmad@gmail.com',
    'SAP',
    'hello'
)
# mapping_request.send_email()

resposne = requests.get('https://cloudtrade.zendesk.com/api/v2/users.json')
print(resposne.content)
