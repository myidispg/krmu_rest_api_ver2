from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.daily_attendance import DailyAttendanceModel
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
                subject_attendance = StudentAttendance.get_attendance_max_present(subject, student.roll_no, student.current_sem)
                attendance_details = {
                    'subject_name': Subjects.get_subject_name(subject),
                    'subject_code': subject_attendance['subject_code'],
                    'max_attendance': subject_attendance['max_attendance'],
                    'present_attendance': subject_attendance['present_attendance']
                }
                student_attendance['subjects'].append(attendance_details)

            return student_attendance
        else:
            return {
                'message': 'No student with that roll number exists.'
            }


class GetStudentAttendanceSemester(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help="Student roll number is required")

    @jwt_required
    def post(self, semester):
        data = GetStudentAttendance.parser.parse_args()

        student = StudentMain.find_by_roll_number(data['roll_no'])
        student_attendance = {
            'roll_no': student.roll_no,
            'semester': semester,
            'subjects': []
        }
        if student:
            subject_code_list = Subjects.find_subject(student.discipline, semester)
            for subject in subject_code_list:
                subject_attendance = StudentAttendance.get_attendance_max_present(subject, student.roll_no, semester)
                attendance_details = {
                    'subject_name': Subjects.get_subject_name(subject),
                    'subject_code': subject_attendance['subject_code'],
                    'max_attendance': subject_attendance['max_attendance'],
                    'present_attendance': subject_attendance['present_attendance']
                }
                student_attendance['subjects'].append(attendance_details)
            return student_attendance
        else:
            return {
                'message': 'No student with that roll number exists.'
            }


class UpdateStudentAttendance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('subject_code', type=str, required=True, help='subject_code cannot be blank')
    parser.add_argument('discipline', type=str, required=True, help='discipline cannot be blank')
    parser.add_argument('semester', type=str, required=True, help='semester cannot be blank')
    parser.add_argument('attendance', type=dict, action='append', required=True, help='attendance cannot be blank')

    @jwt_required
    def post(self):
        data = UpdateStudentAttendance.parser.parse_args()
        attendance = data['attendance']

        for student in attendance:
            # roll_no = student['roll_no']
            # present = student['present']
            daily_attendance = DailyAttendanceModel(student['roll_no'], data['subject_code'], data['semester'],
                                                    student['date'], student['day'], student['status'])
            daily_attendance.save_to_db()
            StudentAttendance.set_attendance(data['subject_code'], data['semester'],
                                             student['roll_no'], student['status'])


class ChangeStudentAttendance(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help='Student Roll No is required')
    parser.add_argument('subject_code', type=str, required=True, help='Subject code is required')
    parser.add_argument('date', type=str, required=True, help='Date of change is required')

    def post(self):
        data = self.parser.parse_args()

        update_happened = DailyAttendanceModel.change_daily_attendance(data['roll_no'], data['subject_code'], data['date'])

        if update_happened['update_happened']:
            StudentAttendance.increase_present_attendance(data['roll_no'], data['subject_code'],
                                                          update_happened['counter'])
            return {
                'message': 'The student has been marked present for the day'
            }
        else:
            return {
                'message': 'The student was already marked present on that day'
            }


