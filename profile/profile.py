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


