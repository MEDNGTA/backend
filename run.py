from flask import Flask, Blueprint
from flask_cors import *
from models import User, Chatroom, Chatevent, Messages, db
from config import config
from flask_socketio import SocketIO,emit,send
from flask_marshmallow import Marshmallow
from flask_login import login_required, current_user,logout_user
from flask_socketio import SocketIO
from random import randint
import datetime

app = Flask(__name__)      
app.config['SECRET_KEY'] = 'mysecret'           #create the Flask app
(mail, bcrypt, db, app, socketio) = config.credit(app)


from auth.auth import auth as auth_bp
app.register_blueprint(auth_bp)

from auth.acc import acc as acc_bp
app.register_blueprint(acc_bp)


from profile.profile import profile as profile_bp
app.register_blueprint(profile_bp)

# from resources.chat import chat as chat_bp
# app.register_blueprint(chat_bp)

@socketio.on("join-room")
def chatroomfun(data):
    print("\n\n\n"+data+"\n\n\n")
    roomcode = randint(10, 99)
    admin = "both"
    date = datetime.datetime.now()
    event = "join a conversation"
    #create room on db  
    user=db.session.query(User).filter_by(username=data).first()
    chatroom = Chatroom(roomcode=roomcode, admin=admin, user=user)
    db.session.add(chatroom)
    db.session.commit()
    chat=db.session.query(Chatroom).filter_by(roomcode=roomcode).first()
    chatevent = Chatevent(date=date, event=event, usersid="1", chatroomevt=chat)
    db.session.add(chatevent)
    db.session.commit()
    return "success !!! " 

@socketio.on("message")
def handleMessage(msg):
    print("\n\nmessage : "+ msg+"\n\n")
    socketio.send(msg, broadcast=True)

if __name__ == '__main__':
   socketio.run(app,debug=True, port=5000, host="0.0.0.0")    #run app in debug mode on port 5000


