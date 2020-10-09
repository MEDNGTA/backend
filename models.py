
from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    email = db.Column(db.String(250))
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