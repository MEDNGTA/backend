# from flask import Blueprint, request, Flask
# from models import User, Chatroom, Chatevent, Messages, db
# from config import config
# from flask_login import login_required, current_user,logout_user
# from flask_socketio import SocketIO
# from random import randint
# import datetime


# if __name__ == "resources.chat" :
#    app = Flask(__name__)
#    chat = Blueprint("chat", __name__)
#    (mail, bcrypt, db, app, socketio) = config.credit(app)

# @socketio.on("connect")
# @login_required
# def connect():
#     socketio.emit('after connect',  {'data':'Lets dance'})

# @socketio.on("join_room")
# @login_required
# def chatroom(data):
#   sender = data["sender"]
#   send = User.query.filter_by(username=sender).all()
#   if send : 
#     roomcode = randint(100000000, 999999999)
#     admin = "both"
#     usersid = send.id 
#     create room on db 
#     chatroom = Chatroom(roomcode=roomcode, admin=admin, users_id= usersid)
#     db.session.add(chatroom)
#     db.session.commit()
#     date = datetime()
#     event = "join a conversation"
    
#     chatroom = Chatroom.query.filter_by(roomcode=roomcode).all()
#     chatroomid = chatroom.id
#     chatevent = Chatevent(date=date, event=event, usersid=usersid, chatroom_id=chatroomid)
#     db.session.add(chatevent)
#     db.session.commit()
#     return "success !!! " 
#     socketio.emit('after join room',  {'data':'success !!!'})


  
