
from flask import Blueprint, request, Flask, url_for, send_from_directory
from models import Profile, db
from config import config
import os
from werkzeug.utils import secure_filename
import json

if __name__ == "profile.profile":
    app = Flask(__name__)
    profile = Blueprint("profile", __name__)
    (mail, bcrypt, db, app, socketio) = config.credit(app)


UPLOAD_FOLDER = 'static/profile-pics-uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@profile.route('/profile-image', methods=['POST'])
def profile_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #return "error 1"
            return {"error": "true", "message": "Bad request, no file part defined"}, 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {"error": True, "message": "Bad request, no file selected"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return {"file_url": url_for('profile.uploaded_file', filename=filename, _external = True)}
        elif not allowed_file(file.filename):
            return { "error": True, "message": "File type not supported, allowed extensions: " + ', '.join(ALLOWED_EXTENSIONS)}, 400

@profile.route('/profile')
def set_profile_data():
    if request.method == 'POST':
        req_data = request.get_json()      # remember to validate data
        birthday = req_data['birthday']
        birthplace = req_data['birthplace']
        nationality = req_data['nationality']
        sex = req_data['sex']
        timezone = req_data['timezone']
        language = req_data['language']
        user_id = req_data['user_id'] #verify that this is the current user's ID, maybe with the tokens

        profile_exists = Profile.query.filter_by(user_id=user_id).all()

        if profile_exists :
            return {"error" : True, "message": "Profile already exists, use http method PUT to modify it"}

        profile = Profile (birthday=birthday, birthplace=birthplace, nationality=nationality, sex=sex, time_zone=time_zone, language=language, user_id = user_id)
        db.session.add(profile)
        db.session.commit()

        return {"error" : False, "message": "Profile created", "profile": profile}

@profile.route('/profile', methods=['GET'])
def get_profile_data_by_profile_id():
    req_data = request.get_json()
    id = req_data['id']

    profile = Profile.query.filter_by(id=id).first()
    if profile:
        return {"error" : False, "message": "Profile found", "profile": profile}
    else:
        return {"error" : True, "message": "Profile not found"}
