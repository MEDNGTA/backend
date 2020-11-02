
from flask import Flask,jsonify, request, abort
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


# app = Flask(__name__) #create the Flask app
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mac:lolipop@localhost/jungle"
ma = Marshmallow()
db = SQLAlchemy()   #you can put value app in creation of tables 


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    firstname = db.Column(db.String(250))
    lastname = db.Column(db.String(250))
    phonenumber = db.Column(db.String(250))
    token = db.Column(db.String(250))

    def __init__(self, username, password, email, firstname, lastname, phonenumber, token):
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phonenumber = phonenumber
        self.token = token

    @property
    def serialize(self):
        return{
           'id':self.id,
           'username':self.username, 
           'password':self.password,
           'email':self.email,
           'firstname':self.firstname,
           'lastname':self.lastname,
           'phonenumber':self.phonenumber,
           'token':self.token,
        }

#db.create_all() #create all tables