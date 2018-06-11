from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.student_attendance import StudentAttendance
from models.subjects import Subjects
from models.student_main import StudentMain


class GetStudentAttendance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help="Student roll number is required")

    @jwt_required
    def post(self):
        data = GetStudentAttendance.parser.parse_args()

        student = StudentMain.find_by_roll_number(data['roll_no'])

        student_attendance = {
            'roll_no': student.roll_no,
            'semester': student.current_sem,
            'subjects': []
        }
        if student:
            subject_code_list = Subjects.find_subject(student.discipline, student.current_sem)
            for subject in subject_code_list:
                student_attendance['subjects'].append(StudentAttendance.get_attendance_max_present(subject,
                                                                                                   student.roll_no,
                                                                                                   student.current_sem))

        return student_attendance
        # return {
        #     'message': 'No student with that roll number exists.'
        # }
