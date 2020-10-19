from flask import Flask,jsonify, request, abort #import main Flask class and request object
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from flask_bcrypt import Bcrypt, check_password_hash
from models import User
from auth.register import register
from random import randint
import json
import jwt

#Configure database and mail credentials ------------------------------------------------------
app = Flask(__name__) #create the Flask app
mail=Mail(app)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mac:lolipop@localhost/jungle"
db = SQLAlchemy(app)
app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"]=587
app.config["MAIL_USERNAME"]="petappdz@gmail.com"
app.config["MAIL_PASSWORD"]="jebnwhiteddxqvpa"
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USE_SSL"]=False
mail = Mail(app)
#register route  ---------------------------------------------------------------------
@app.route('/json-reg', methods=['POST', 'GET']) #GET requests will be blocked
def json_reg():
 if request.method == 'POST':
    req_data = request.get_json()      # remember to validate data
    return register.main_route(req_data, bcrypt, db, mail)
    
<<<<<<< HEAD
=======
   
@app.route('/update-reg', methods=['POST', 'GET'])
def update_reg():
 if request.method == 'POST':
  req_data = request.get_json()      # remember to validate data 
  return register.reg_conf(req_data, db)

@app.route('/form-example')
def formexample():
    return 'Todo...'

>>>>>>> update response to registration

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000p


