# environment variables 
import os
from dotenv import load_dotenv
load_dotenv()

import sendgrid
from email.message import EmailMessage
from sendgrid.helpers.mail import Mail, Email, To, Content

from logic import sqlQueries

receiver_email = os.getenv('EMAIL')
# password = os.getenv('PASSWORD')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
sender = os.getenv('SENDER')

def send_email(message):
    send_grid = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
   
    users = sqlQueries.getUsers()
   
    subject = "Notify Company Updates"
    from_email = Email(sender)  
    
    for tuple in users:
        email = tuple[0]
        to_email = To(email)  
        content = Content("text/plain", message)
        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        send_grid.client.mail.send.post(request_body=mail_json)
    
    
def parsing_error(company):
    send_grid = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    from_email = Email(sender)  
    to_email = To(receiver_email)  

    subject = "Scrapping Error"
    
    message = f"Error scrapping company {company}"
    print(f"Error scrapping company {company}")
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    send_grid.client.mail.send.post(request_body=mail_json)
    
def test_email():
    send_grid = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

    from_email = Email(sender)  
    to_email = To(receiver_email)  

    subject = "Company Updates"
    
    message = "This is test message "
     
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    send_grid.client.mail.send.post(request_body=mail_json)
    
        
def emailConfirmation(email):
    
    send_grid = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

    from_email = Email(sender)  
    to_email = To(email)  

    subject = "Notify - Please Confirm Joining"
    
    
    # link = 
    
    
    message = "Use the following link the confirm your addition to mailing list. " + time.strftime("%A, %d. %B %Y %I:%M:%S %p")
     
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    send_grid.client.mail.send.post(request_body=mail_json)
    

def contact(email,name, msg):
    send_grid = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

    from_email = Email(email)  
    to_email = To(receiver_email)  

    subject = f"Contact About Notify App - from {name}"
    content = Content("text/plain", msg)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    send_grid.client.mail.send.post(request_body=mail_json)
    
# send_email([["Google", "SWE"], ["reddit", "SWE"]])