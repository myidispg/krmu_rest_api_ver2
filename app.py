from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.assignment import MaterialUploadResource
from resources.student_attendance import GetStudentAttendance, GetStudentAttendanceSemester, UpdateStudentAttendance
from resources.student_main import *
from resources.student_marks import GetStudentMarks, GetStudentMarksSemester
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
api.add_resource(GetStudentAttendanceSemester, '/api/get_student_semester_attendance/<string:semester>')
api.add_resource(UpdateStudentAttendance, '/api/update_student_attendance')
api.add_resource(GetStudentMarks, '/api/get_student_marks')
api.add_resource(GetStudentMarksSemester, '/api/get_student_semester_marks/<string:semester>')

api.add_resource(TeacherRegister, '/api/teacher/teacher_register')
api.add_resource(TeacherProfilePicture, '/api/teacher/<string:teacher_code>/profile_picture')
api.add_resource(TeacherLogin, '/api/teacher/teacher_login')
api.add_resource(MaterialUploadResource, '/api/teacher/upload_study_material')

api.add_resource(TokenRefresh, '/api/token_refresh')

if __name__ == '__main__':
    app.run()
