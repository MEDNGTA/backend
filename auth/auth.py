from flask import Blueprint, request, Flask, jsonify
from flask_mail import *
from flask_cors import *
from models import Users,db,Tokens
from flask_bcrypt import check_password_hash
from resources.mailing import mailing
from flask_login import login_required, LoginManager, current_user,logout_user
from random import randint
from config import app, mail, db, socketio, bcrypt
from flask_socketio import SocketIO
import json
import jwt
import datetime



if __name__ == "auth.auth" :
  auth = Blueprint("auth", __name__)

@auth.route('/json-reg', methods=['POST']) 
def json_reg():
 if request.method == 'POST':
    req_data = request.get_json()     # remember to validate data
    username = req_data['username']
    password = req_data['password']  
    password = bcrypt.generate_password_hash(password).decode('utf-8') 
    email = req_data['email']
    firstname = req_data['firstname']
    lastname = req_data['lastname']
    phonenumber = req_data['phonenumber']
    reg_obj_un= Users.query.filter_by(username=username).first() #verify if the username exist on database
    reg_obj_em= Users.query.filter_by(email=email).first()       #verify if the email exist on database
    if reg_obj_un or reg_obj_em :
        return jsonify({"message":"Change email or Username"}),401
    user=Users(username=username, password=password, email=email, firstname=firstname, lastname=lastname, phonenumber=phonenumber)
    db.session.add(user)
    db.session.commit()        
    conf_code = randint(100000, 999999) 
    url = "http://127.0.0.1:5000/"+conf_code                          
    mailing.sendmail_reg(email, conf_code, url, mail)
    return jsonify({ "email": email, "code": conf_code, "url": url,"msg":"success register please confirm code"}),200
    

@auth.route('/json-login', methods=['POST'])
def json_login():
 if request.method == 'POST':
    req_data = request.get_json()      # remember to validate data 
    email = req_data['email'] 
    if email :
       password = req_data['password']  
       if  Users.query.filter_by(email=email).first() is not None :
           obj =Users.query.filter_by(email=email).first()
           crypted = obj.password
       else:
           return jsonify({"msg":"username invalid"}),403
       if bcrypt.check_password_hash(crypted, password):
         token = jwt.encode({'user': email, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'], algorithm='HS256').decode("utf-8")
         expire_t = datetime.datetime.utcnow()+datetime.timedelta(minutes=60)
         create_t = datetime.datetime.utcnow()
         refrechToken = jwt.encode({'user': email, 'exp':datetime.datetime.utcnow()+datetime.timedelta(days=240)}, app.config['SECRET_KEY'], algorithm='HS256').decode("utf-8")
         expire_rt = datetime.datetime.utcnow()+datetime.timedelta(days=240)
         create_rt = datetime.datetime.utcnow()
         tokens = Tokens(token = token, expire_t = expire_t, create_t = create_t, refrechToken = refrechToken, expire_rt = expire_rt, create_rt = create_rt, usertkn = obj)
         db.session.add(tokens)
         db.session.commit() 
         return jsonify({"token":token,"expire_t": expire_t,"refrechToken":refrechToken,"expire_rt":expire_rt}),200
       else :
         return jsonify({"msg":"password invalid"}),403
    else :
      return jsonify({"msg":"Login information empty check and retry"}),403

@auth.route('/update-reg', methods=['POST'])
def update_reg():
 if request.method == 'POST':
    req_data = request.get_json()   
    token = req_data['code']
    email = req_data['email'] 
    user= Users.query.filter_by(email=email).first() #select user
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
    user= Users.query.filter_by(username=username, email=email, phonenumber=phonenumber).first() 
    if user :
      url = "http://127.0.0.1:5000/"+user.token                          
      mailing.sendmail_fp(email, url, mail)
      return jsonify({"userid": user.id, "email": email, "url": url}),200
    else :
      return jsonify({"msg":"bad recover information"}),403

@auth.route('/fp-conf', methods=['POST'])
def fp_conf():
 if request.method == 'POST':
    req_data = request.get_json()   
    userid = req_data['userid']
    email = req_data['email']
    user= Users.query.filter_by(id=userid, email=email).first()
    if user :
      return "confirmed password"

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
  logout_user()
  return "user loggin out"

