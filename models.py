
from flask import Flask,jsonify, request, abort
from marshmallow import Schema, fields, pre_load, validate
from config import app, mail, db, socketio, bcrypt
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

   #(mail, bcrypt, db, app, socketio) = config.credit(app)
   #you can put value app in creation of tables 


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    firstname = db.Column(db.String(250))
    lastname = db.Column(db.String(250))
    phonenumber = db.Column(db.String(250))
    confUser = db.Column(db.Boolean, nullable=False)
    
    


class Chatrooms(db.Model):
    __tablename__ = 'chatroom'

    id = db.Column(db.Integer, primary_key=True)
    roomcode = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.String(250), nullable=False)
    people = db.Column(JSONB, nullable=False) 


class Chatevents(db.Model):
    __tablename__ = 'chatevent'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    event = db.Column(db.String(250), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    userevt = db.relationship(
        Users,
        backref=db.backref('chatevent',
                         uselist=True,
                         cascade='delete,all'))
    chatroom_id = db.Column(db.Integer, db.ForeignKey("chatroom.id"))
    chatroomevt = db.relationship(
        Chatrooms,
        backref=db.backref('chatevent',
                         uselist=True,
                         cascade='delete,all'))


class Messages(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    sender= db.Column(db.String(250), nullable=False)
    date_msg = db.Column(db.DateTime, nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey("chatroom.id"))
    chatroommsg = db.relationship(
        Chatrooms,
        backref=db.backref('message',
                         uselist=True,
                         cascade='delete,all'))
    

class Tokens(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(250), unique=True, nullable=False)
    expire_t = db.Column(db.DateTime, nullable=False)
    create_t = db.Column(db.DateTime, nullable=False)
    refrechToken = db.Column(db.String(250), unique=True, nullable=False)
    expire_rt = db.Column(db.DateTime, nullable=False)
    create_rt = db.Column(db.DateTime, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    usertkn = db.relationship(
        Users,
        backref=db.backref('token',
                         uselist=True,
                         cascade='delete,all'))

class Sessions(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    opening_date = db.Column(db.String(250), unique=True, nullable=False)
    closing_date = db.Column(db.DateTime, nullable=False)
    

  #db.create_all() #create all tables