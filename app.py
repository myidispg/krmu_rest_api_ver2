from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.student_main import *
app = Flask(__name__)

UPLOAD_FOLDER_PROFILE_PICTURES = "/profile-pictures"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['PROPOGATE_EXCEPTIONS'] = True
app.config['UPLOAD_FOLDER_PROFILE_PICTURES'] = UPLOAD_FOLDER_PROFILE_PICTURES
app.secret_key = 'KRMU_BACK_APIs'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(StudentRegister, '/api/student_register')
api.add_resource(StudentProfilePicture, '/api/<string:roll_no>/profile_picture')

if __name__ == '__main__':
    app.run()
