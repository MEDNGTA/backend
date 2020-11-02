from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from flask_cors import *
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
import os

#Configure database and mail credentials ------------------------------------------------------
class config():
    def credit(app):
       basedir = os.path.abspath(os.path.dirname(__file__))
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
       CORS(app)
       app.config["Access-Control-Allow-Origin"] = "http://127.0.0.1:5000"
       socketio = SocketIO(app, cors_allowed_origins="*")
       return mail, bcrypt, db, app, socketio
    
    
    