from flask import Flask
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from app import app

@app.route("/send_mail")
def send():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    email_address = os.getenv('EMAIL_ADDRESS')
    app_password = os.getenv('APP_PASSWORD')
    server.login(email_address, app_password)
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = 'bena.yalla@yahoo.com'
    msg['Subject'] = 'Test Email'
    message = 'This is the body of the test email.'
    msg.attach(MIMEText(message))
    server.send_message(msg)
    server.quit()
    return "Mail sent successfully!"
