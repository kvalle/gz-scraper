import smtplib
import ssl
import os

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "gz.scraper@gmail.com"
receiver_email = "kjetil.valle@gmail.com"
password = os.environ['GZ_SCRAPER_EMAIL_PASSWORD']
message_template = """\
Subject: {subject}

{body}"""

def format_message(subject, body):
    return message_template.format(subject=subject, body=body)

def send(subject, body):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        message = format_message(subject, body)
        server.sendmail(sender_email, receiver_email, message)
