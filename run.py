from flask import Flask,jsonify, request, abort #import main Flask class and request object
from flask_sqlalchemy import SQLAlchemy
from models import User
from flask_bcrypt import Bcrypt, check_password_hash
from resources.mail import mail
from random import randint
import json
import jwt

#Configure database credentials ------------------------------------------------------
app = Flask(__name__) #create the Flask app
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mac:lolipop@localhost/jungle"
db = SQLAlchemy(app)

#register route  ---------------------------------------------------------------------
@app.route('/json-reg', methods=['POST', 'GET']) #GET requests will be blocked
def json_reg():
  if request.method == 'POST':
    req_data = request.get_json()      # remember to validate data
    username = req_data['username']
    password = req_data['password']  
    password = bcrypt.generate_password_hash(password).decode('utf-8') #remember to crypt password
    check = bcrypt.check_password_hash(password, uspass)
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
    mail.sendmail_reg(email, conf_code, url)
    return json.dumps({"token": token, "email": email, "code": conf_code, "url": url})  # return to frontend in the same address /json-reg
   #------------------------------------------------------------------------------------ 
    
   
@app.route('/')
def query_example():
    return 'Todo...'

@app.route('/form-example')
def formexample():
    return 'Todo...'


if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000p


