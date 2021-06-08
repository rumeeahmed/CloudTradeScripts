from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
import smtplib
import shutil
import os


class Emailer:

    def __init__(self, from_address: str, from_password: str, to_address: str, file_path: str):
        """

        :param from_address: The email address to send the message from.
        :param from_password: The password associated with the sending email address.
        :param to_address: The email address to send the message to.
        :param file_path: The file path of any attachment to send.
        """
        self.from_address = from_address
        self.from_password = from_password
        self.to_address = to_address
        self.file_path = file_path

    def _prepare_mime(self):
        """
        Prepare and configure the `MIMEMultipart` object so that it can contain email data and attachments. The From, To
        and subject fields represent the header data of the email. Then attach the MIMEText object to the
        `MIMEMultipart` object - which contains the body of text to include in the email.
        :return: None
        """
        self.msg = MIMEMultipart()
        self.msg['From'] = self.from_address
        self.msg['To'] = self.to_address
        self.msg['Subject'] = 'New File'
        self.msg.attach(MIMEText('Please see attached file forwarded from the server'))

    def _attach_part(self):
        """
        Attach the file to the `MIMEMultipart` object. Instantiate a MIMEBase object that will contain the attachment.
        Open the file and read it in binary, set the `MIMEBase` object's payload as the content of the file. Encode the
        `MIMEBase` in base64 and then add the headers to it. Then attach the `MIMEBase` into the `MIMEMultipart` object.
        :return: None
        """
        self._prepare_mime()

        part = MIMEBase('application', "octet-stream")
        with open(self.file_path, 'rb') as attachment_file:
            part.set_payload(attachment_file.read())

        encoders.encode_base64(part)
        part.add_header(f'Content-Disposition', 'attachment; filename="{}"'.format(Path(self.file_path).name))
        self.msg.attach(part)

    def send_email(self, host: str,  port: int):
        """
        Send the email from self.from_address` to `self.to_address`. Prepare the `MIMEMultipart` object and attach any
        files. Open up a connection to the mail server, secure the connection, login with credentials and then send the
        email.
        :param host: The SMTP host server of the `self.from_address` attribute.
        :param port: The SMTP port of the `self.from_address` attribute.
        :return: None
        """
        self._attach_part()
        with smtplib.SMTP(host, port) as connection:
            connection.connect(host, port)
            connection.starttls()
            connection.login(self.from_address, self.from_password)
            connection.sendmail(self.from_address, self.to_address, msg=self.msg.as_string())


attachment_directory = '/Users/rumeeahmed/Documents/CloudTradeScripts/Countess of Chester Emailer/pdfs'
move_path = '/Users/rumeeahmed/Documents/CloudTradeScripts/Countess of Chester Emailer/moved_pdfs'
files = os.listdir(attachment_directory)

from_address = 'rumeeahmed.test@gmail.com'
password = ''
to_address = 'rumeeahmad@gmail.com'

for file in files:
    emailer = Emailer(from_address, password, to_address, f'{attachment_directory}/{file}')
    emailer.send_email('smtp.gmail.com', 587)
    shutil.move(f'{attachment_directory}/{file}', move_path)
