from app import app, mail
from flask_mail import Mail
from mailbox import Message

@app.route("/send_mail")
def send():
    mail_message = Message()
    mail_message.subject = 'Hi! Don\'t forget to follow me for more articles!'
    mail_message.recipients = ['bena.yalla@gmail.com']
    mail_message.sender = 'menna20.samir@gmail.com'
    mail_message.body = "This is a test"
    mail.send(mail_message)
    return "Mail has sent"