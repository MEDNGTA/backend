from flask import Flask, Blueprint
from flask_cors import *
from models import Users, Chatrooms, Chatevents, Messages, db
from config import config
from flask_socketio import SocketIO,emit,send
from flask_marshmallow import Marshmallow
from flask_login import login_required, LoginManager, current_user,logout_user
from flask_socketio import SocketIO
from random import randint
import datetime


app = Flask(__name__)      
app.config['SECRET_KEY'] = 'mysecret'          #create the Flask app
# login_manager = LoginManager()
# login_manager.init_app(app)
(mail, bcrypt, db, app, socketio) = config.credit(app)


from auth.auth import auth as auth_bp
app.register_blueprint(auth_bp)

from auth.acc import acc as acc_bp
app.register_blueprint(acc_bp)

# from resources.chat import chat as chat_bp
# app.register_blueprint(chat_bp)

@socketio.on("create-room")
def chatroomfun(data):
    sender = data["sender"]
    reciever = data["reciever"]
    roomcode = randint(10, 99)
    admin = "both"
    date = datetime.datetime.now()
    event_send = "open a conversation"
    event_reciev = "joining a conversation "
    #create room on db  
    user_send=db.session.query(Users).filter_by(username=sender).first()
    user_reciev=db.session.query(Users).filter_by(username=reciever).first()
    people = {"user_one":user_send.username, "user_two":user_reciev.username}
    people2 = {"user_one":user_reciev.username, "user_two":user_send.username}
    if db.session.query(Chatrooms).filter_by(people=people).first() or db.session.query(Chatrooms).filter_by(people=people2).first() :
        return "This conversation existe"
    else :
      chatroom = Chatrooms(roomcode=roomcode, admin=admin, people=people )
      db.session.add(chatroom)
      db.session.commit()
      chat=db.session.query(Chatrooms).filter_by(roomcode=roomcode).first()
      chatevent_send= Chatevents(date=date, event=event_send, userevt=user_send, chatroomevt=chat)
      chatevent_reciev= Chatevents(date=date, event=event_reciev, userevt=user_reciev, chatroomevt=chat) 
      db.session.add_all([chatevent_send, chatevent_reciev])
      db.session.commit()
      return "success !!! " 
    

def getuser():
    users_on = db.session.query(Chatrooms).filter_by(roomcode=roomcode).first()



@socketio.on("message")
def handleMessage(msg):
    print("\n\nmessage : "+ msg+"\n\n")
    socketio.send(msg, broadcast=True)

if __name__ == '__main__':
   socketio.run(app,debug=True, port=5000, host="0.0.0.0")    #run app in debug mode on port 5000


