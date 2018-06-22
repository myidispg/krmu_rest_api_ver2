from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.assignment import MaterialUploadResource, MaterialSubmissionResource, StudentAssignmentMarksResource, \
    TeacherAllAssignmentResource, TeacherSingleAssignmentFileResource, \
    StudentSingleAssignmentResource, TeacherSingleAssignmentResource, StudentAllAssignmentsResource
from resources.daily_attendance import GetDailyAttendanceStudent
from resources.events import EventsRegistration, EventFile, EventSingle, EventsAll
from resources.student_attendance import GetStudentAttendance, GetStudentAttendanceSemester, UpdateStudentAttendance, \
    ChangeStudentAttendance
from resources.student_main import *
from resources.student_marks import GetStudentMarks, GetStudentMarksSemester
from resources.teacher_main import TeacherRegister, TeacherProfilePicture, TeacherLogin
from resources.time_table import TimeTableStudent, TimeTableTeacher

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
api.add_resource(MaterialSubmissionResource, '/api/submit_material_student')
api.add_resource(StudentSingleAssignmentResource, '/api/get_single_assignment/<string:material_code>&<string:roll_no>')
api.add_resource(StudentAllAssignmentsResource, '/api/get_all_assignments')
api.add_resource(TimeTableStudent, '/api/time_table_student')
api.add_resource(GetDailyAttendanceStudent, '/api/get_daily_attendance/q=<string:roll_no>&q=<string:subject_code>')

api.add_resource(TeacherRegister, '/api/teacher/teacher_register')
api.add_resource(TeacherProfilePicture, '/api/teacher/<string:teacher_code>/profile_picture')
api.add_resource(TeacherLogin, '/api/teacher/teacher_login')
api.add_resource(MaterialUploadResource, '/api/teacher/upload_study_material')
api.add_resource(StudentAssignmentMarksResource, '/api/teacher/assignment_marks_upload')
api.add_resource(TeacherAllAssignmentResource, '/api/teacher/get_all_assignments_teacher_code/<string:teacher_code>')
api.add_resource(TeacherSingleAssignmentResource, '/api/teacher/get_single_assignment/<string:material_code>')
api.add_resource(TeacherSingleAssignmentFileResource, '/api/teacher/get_single_assignment_file/<string:material_code>')
api.add_resource(TimeTableTeacher, '/api/teacher/time_table_teacher')
api.add_resource(ChangeStudentAttendance, '/api/teacher/change_student_attendance')

api.add_resource(TokenRefresh, '/api/token_refresh')

api.add_resource(EventsRegistration, '/api/events/registration')
api.add_resource(EventFile, '/api/events/file/<string:event_code>')
api.add_resource(EventSingle, '/api/events/single/<string:event_code>')
api.add_resource(EventsAll, '/api/events/get_all')


if __name__ == '__main__':
    app.run()
