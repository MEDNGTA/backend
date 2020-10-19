
from flask_sqlalchemy import SQLAlchemy
from models import User
from flask_bcrypt import Bcrypt, check_password_hash
from resources.mailing import mailing
from random import randint
import json
import jwt


class register():
 def main_route(req_data, bcrypt, db, mail):

    username = req_data['username']
    password = req_data['password']  
    password = bcrypt.generate_password_hash(password).decode('utf-8') #remember to crypt password
    #check = bcrypt.check_password_hash(password, uspass)
    email = req_data['email']
    firstname = req_data['firstname']
    lastname = req_data['lastname']
    phonenumber = req_data['phonenumber']
    token = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256').decode("utf-8")
   #------------------------------------------------------------------------------------
    reg_obj_un= User.query.filter_by(username=username).all() #verify if the username exist on database
    reg_obj_em= User.query.filter_by(email=email).all()       #verify if the email exist on database
   #------------------------------------------------------------------------------------
    if reg_obj_un or reg_obj_em :
        return "Change email or Username"
   #------------------------------------------------------------------------------------
    user=User(username=username, password=password, email=email, firstname=firstname, lastname=lastname, phonenumber=phonenumber, token=token)
    db.session.add(user)
    db.session.commit()        #insert user into database
    conf_code = randint(100000, 999999) 
    url = "http://127.0.0.1:5000/"+token                          
    mailing.sendmail_reg(email, conf_code, url, mail)
    return json.dumps({"token": token, "email": email, "code": conf_code, "url": url})  # return to frontend in the same address /json-reg
   #------------------------------------------------------------------------------------ 
 def reg_conf(req_data, db):
  token = req_data['token']
  email = req_data['email'] 
  user= User.query.filter_by(email=email).first() #select user
  user.email=email # change later when we change table user to confirmed user attribute
  user.token=token
  db.session.commit()
  return "confirmed users"