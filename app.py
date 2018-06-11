from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.student_attendance import GetStudentAttendance
from resources.student_main import *
from resources.teacher_main import TeacherRegister, TeacherProfilePicture, TeacherLogin

app = Flask(__name__)

app.config['PROPOGATE_EXCEPTIONS'] = True
# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = {'access', 'refresh'}
app.secret_key = 'KRMU_BACK_APIs'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(StudentRegister, '/api/student_register')
api.add_resource(StudentProfilePicture, '/api/<string:roll_no>/profile_picture')
api.add_resource(StudentLogin, '/api/student_login')
api.add_resource(GetStudentAttendance, '/api/get_student_attendance')

api.add_resource(TeacherRegister, '/api/teacher/teacher_register')
api.add_resource(TeacherProfilePicture, '/api/teacher/<string:teacher_code>/profile_picture')
api.add_resource(TeacherLogin, '/api/teacher/teacher_login')



if __name__ == '__main__':
    app.run()
