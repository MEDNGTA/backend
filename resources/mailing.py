from flask import render_template
from flask_mail import Mail, Message
import os
import smtplib

   
class mailing():
  def sendmail_reg(email, conf_code, url, mail):
    mymail = "petappdz@gmail.com"
    subject = "Welcome to our application"
    recip = []
    recip.append(email)

    msg = Message(subject=subject, sender=mymail, recipients=recip)
    msg.body = ""
    msg.html = render_template("mail_reg.html", conf_code=conf_code, url=url)
    mail.send(msg)
      