# Countess of Chester Emailer

This program is designed to email over a file in a directory. The `Emailer` class sends 
one file over via email and therefore a loop is needed to send over multiple files. 

First initialise the variables in reference to the directory that contains the files for the 
program to read, then create a list of files in that directory and finally a path to move the 
files that have been sent.
```python
attachment_directory = '/Users/rumeeahmed/Documents/CloudTradeScripts/Countess of Chester Emailer/pdfs'
move_path = '/Users/rumeeahmed/Documents/CloudTradeScripts/Countess of Chester Emailer/moved_pdfs'
files = os.listdir(attachment_directory)
```

Then initialise the variables for the email details:
```python
from_address = ''
password = ''
to_address = ''
subject = ''
```

Loop over the files list and then instantiate an Emailer object using the
`from_address`, `password`, `to_address`, `subject` and the file path as its
parameters. Use the send method and input the email SMTP HOST and PORT as
parameters and finally move the sent PDF to another directory.
```python
for file in files:
    emailer = Emailer(from_address, password, to_address, subject, f'{attachment_directory}/{file}')
    emailer.send_email('smtp.gmail.com', 587)
    shutil.move(f'{attachment_directory}/{file}', move_path)

```