import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(message):
    host = os.environ["MAIL_HOST"]
    user = os.environ["MAIL_USER"]
    password = os.environ["MAIL_PASS"]
    port = int(os.environ["MAIL_PORT"])
    recipient = os.environ["MAIL_RECIPIENT"]

    msg = MIMEMultipart()
    msg["From"] = user
    msg["To"] = recipient
    msg["Subject"] = "An update from scraper"
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP(host, port)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(user, password)
    mailServer.sendmail(user, recipient, msg.as_string())
    mailServer.close()


def main():
    send_mail("Hello World!")


if __name__ == "__main__":
    main()
