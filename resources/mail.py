import os
import smtplib

class mail():
  def sendmail_reg(mail, conf_code, url):
    mymail = "petappdz@gmail.com"
    mypass = "icuuyvcgbfixmzqe"
    with smtplib.SMTP("smtp.gmail.com",587) as smtp:
      smtp.ehlo()
      smtp.starttls()
      smtp.ehlo()

      smtp.login(mymail, mypass)

      subject = "Welcome to our application"
      head = "Hello subscriber,"
      bcode = "Your activation code is"+str(conf_code)
      ucode = "Your activation link is "+str(url)

      msg = f"Subject: {subject}\n\n{head}\n\n{bcode}\n{ucode}"

      smtp.sendmail(mymail, mail, msg)