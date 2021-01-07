
from flask import Blueprint, request, Flask, url_for, send_from_directory
from models import Event, db, Participant
from config import config
import os
from werkzeug.utils import secure_filename
import json

if __name__ == "event.event":
    app = Flask(__name__)
    event = Blueprint("event", __name__)
    (mail, bcrypt, db, app, socketio) = config.credit(app)

UPLOAD_FOLDER = 'static/event-pics-uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@event.route('/event/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@event.route('/event-image', methods=['POST'])
def event_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return {"error": "true", "message": "Bad request, no file part defined"}, 400
        file = request.files['file']
        if file.filename == '':
            return {"error": True, "message": "Bad request, no file selected"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return {"file_url": url_for('event.uploaded_file', filename=filename, _external = True)}
        elif not allowed_file(file.filename):
            return { "error": True, "message": "File type not supported, allowed extensions: " + ', '.join(ALLOWED_EXTENSIONS)}, 400

@event.route('/event')
def add_event():
    if request.method == 'POST':
        req_data = request.get_json()
        code = req_data['code']
        datetime = req_data['datetime']
        time_zone = req_data['time_zone']
        latitude = req_data['latitude']
        longitude = req_data['longitude']
        status = req_data['status']
        type = req_data['type']
        user_id = req_data['user_id'] #admin
        description= req_data['description']
        event = Event (code=code, datetime=datetime, time_zone=time_zone,
                       latitude=latitude, longitude=longitude, status=status, type = type,
                       description=description,user_id=user_id)
        db.session.add(event)
        db.session.commit()
        participant = Participant(id_event=event.id_event, id_user=user_id, type='Admin',
                                  datetime=datetime)
        db.session.add(participant)
        db.session.commit()
        return {"error" : False, "message": "Event created", "event": event}

@event.route('/event_participant')
def add_participant_toevent():
    if request.method == 'POST':
        req_data = request.get_json()
        id_event = req_data['id_event']
        id_user = req_data['user_id']
        type = req_data['type']#user tyoe participant or organizer
        datetime = req_data['datetime']
        latitude = req_data['latitude'] #home user
        longitude = req_data['longitude']  #home user

        event = Event.query.filter_by(id=id_event).first()
        if event:
            participant = Participant (id_event=id_event, id_user=id_user, type=type,
                           datetime=datetime, longitude=longitude, latitude=latitude)
            db.session.add(participant)
            db.session.commit()
            return {"error" : False, "message": "participant added", "participant": participant}
        else:
            return {"error" : True, "message": "Event not found"}

@event.route('/event_update')
def update_event():
    if request.method == 'POST':
        event = Event.query.filter_by(id=request.get_json().id_event).first()
        #verifier user !!!!
        if event and event.user_id == request.get_json()['user_id']:
            req_data = request.get_json()
            #event.code = req_data['code'] only once
            event.datetime = req_data['datetime']
            event.time_zone = req_data['time_zone']
            event.latitude = req_data['latitude']
            event.longitude = req_data['longitude']
            event.status = req_data['status']
            event.type = req_data['type']
            #event.user_id = req_data['user_id'] #admin only once
            event.description= req_data['description']
            # event = Event (code=code, datetime=datetime, time_zone=time_zone,
            #                latitude=latitude, longitude=longitude, status=status, type = type,
            #                description=description,user_id=user_id)
            #db.session.add(event)
            db.session.commit()
            return {"error" : False, "message": "Event updated", "event": event}
        else:
            return {"error" : True, "message": "Event not found"}
