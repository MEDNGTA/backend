from flask import Blueprint, request, Flask
from flask_mail import *
from flask_cors import *
from models import User,db
from flask_bcrypt import check_password_hash
from resources.mailing import mailing
from flask_login import login_required, current_user,logout_user
from random import randint
from config import config
from flask_socketio import SocketIO
import json
import jwt

if __name__ == "auth.auth" :
  app = Flask(__name__)
  auth = Blueprint("auth", __name__)
  (mail, bcrypt, db, app, socketio) = config.credit(app)

@auth.route('/json-reg', methods=['POST']) 
def json_reg():
 
 if request.method == 'POST':
    req_data = request.get_json()      # remember to validate data
    username = req_data['username']
    password = req_data['password']  
    password = bcrypt.generate_password_hash(password).decode('utf-8') 
    email = req_data['email']
    firstname = req_data['firstname']
    lastname = req_data['lastname']
    phonenumber = req_data['phonenumber']
    token = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256').decode("utf-8")
   
    reg_obj_un= User.query.filter_by(username=username).all() #verify if the username exist on database
    reg_obj_em= User.query.filter_by(email=email).all()       #verify if the email exist on database
   
    if reg_obj_un or reg_obj_em :
        return "Change email or Username"
   
    user=User(username=username, password=password, email=email, firstname=firstname, lastname=lastname, phonenumber=phonenumber, token=token)
    db.session.add(user)
    db.session.commit()        
    conf_code = randint(100000, 999999) 
    url = "http://127.0.0.1:5000/"+token                          
    mailing.sendmail_reg(email, conf_code, url, mail)
    return json.dumps({"token": token, "email": email, "code": conf_code, "url": url}) 
    

@auth.route('/json-login', methods=['POST'])
def json_login():
 if request.method == 'POST':
    req_data = request.get_json()      # remember to validate data 
    username = req_data['username']
    email = req_data['email']
    if username or email:
       password = req_data['password']  
       token = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256').decode("utf-8")

       log_obj_un= User.query.filter_by(username=username).first() #verify if the username exist on database
       log_obj_em= User.query.filter_by(email=email).first() 

       if bcrypt.check_password_hash(log_obj_un.password, password) or bcrypt.check_password_hash(log_obj_em.password, password) :
         # create session with token variable
         return "create session"
       else :
         return "username or password invalid"


    else :
      return "Login information empty check and retry"

@auth.route('/update-reg', methods=['POST'])
def update_reg():
 if request.method == 'POST':
    req_data = request.get_json()   
    token = req_data['token']
    email = req_data['email'] 
    user= User.query.filter_by(email=email,token=token).first() #select user
    if user :
     # change later when we change table user to confirmed user attribute
     #db.session.commit()
     return "confirmed users"

@auth.route('/forgotpass', methods=['POST'])
def forgotpass():
 if request.method == 'POST':
    req_data = request.get_json()   
    username = req_data['username']
    email = req_data['email']
    phonenumber = req_data['phonenumber'] 
    user= User.query.filter_by(username=username, email=email, phonenumber=phonenumber).first() 
    if user :
      url = "http://127.0.0.1:5000/"+user.token                          
      mailing.sendmail_fp(email, url, mail)
      return json.dumps({"userid": user.id, "email": email, "url": url}) 

@auth.route('/fp-conf', methods=['POST'])
def fp_conf():
 if request.method == 'POST':
    req_data = request.get_json()   
    userid = req_data['userid']
    email = req_data['email']
    user= User.query.filter_by(id=userid, email=email).first()
    if user :
      return "confirmed password"

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
  logout_user()
  return "user loggin out"

