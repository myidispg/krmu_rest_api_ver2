from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.student_main import *
app = Flask(__name__)

app.config['PROPOGATE_EXCEPTIONS'] = True
app.secret_key = 'KRMU_BACK_APIs'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(StudentRegister, '/api/student_register')
api.add_resource(StudentProfilePicture, '/api/<string:roll_no>/profile_picture')

if __name__ == '__main__':
    app.run()
