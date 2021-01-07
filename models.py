
from flask import Flask,jsonify, request, abort
from marshmallow import Schema, fields, pre_load, validate
from config import config
from flask_marshmallow import Marshmallow

from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

app = Flask(__name__) #create the Flask app
(mail, bcrypt, db, app, socketio) = config.credit(app)
   #you can put value app in creation of tables 


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
    #sessions = db.relationship("Session", backref="usefrom")

    # def __init__(self, username, password, email, firstname, lastname, phonenumber, token):
    #     self.username = username
    #     self.password = password
    #     self.email = email
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.phonenumber = phonenumber
    #     self.token = token

    


class Chatroom(db.Model):
    __tablename__ = 'chatroom'

    id = db.Column(db.Integer, primary_key=True)
    roomcode = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.String(250), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship(
        User,
        backref=db.backref('chatroom',
                         uselist=True,
                         cascade='delete,all'))

class Chatevent(db.Model):
    __tablename__ = 'chatevent'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    event = db.Column(db.String(250), nullable=False)
    usersid = db.Column(db.Integer, nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey("chatroom.id"))
    chatroomevt = db.relationship(
        Chatroom,
        backref=db.backref('chatevent',
                         uselist=True,
                         cascade='delete,all'))


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    sender= db.Column(db.String(250), nullable=False)
    date_msg = db.Column(db.DateTime, nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey("chatroom.id"))
    chatroommsg = db.relationship(
        Chatroom,
        backref=db.backref('messages',
                         uselist=True,
                         cascade='delete,all'))

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(250), nullable=True)
    birthday = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.String(250), nullable=True) # Why we need this? this is weird nobody will accept giving this info
    nationality = db.Column(db.String(250), nullable=True) # Same as above this is a pets' app not a governemental visa application form
    sex = db.Column(db.String(50), nullable=True)
    time_zone = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(250), nullable=True)
    datetime = db.Column(db.Date, nullable=False) #event date
    time_zone = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Double, nullable=False)
    longitude = db.Column(db.Double, nullable=False )
    status = db.Column(db.String(50), nullable=False) #actif / inactif
    type = db.Column(db.String(50), nullable=False) #rescue / walk/ talkih
    description = db.Column(db.String(250), nullable=True)

class Participant(db.Model):
    __tablename__ = 'participant'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.Date, nullable=False) #joining date
    latitude = db.Column(db.Double, nullable=False) #trick to get users home adress))
    longitude = db.Column(db.Double, nullable=False) #trick to get users home adress))
    type = db.Column(db.String(50), nullable=True) #admin /organiser / participant/other
    id_event = db.Column(db.Integer, db.ForeignKey("event.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"))

  #db.create_all() #create all tables
