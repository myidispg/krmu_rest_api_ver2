from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.student_marks import StudentMarks
from models.subjects import Subjects
from models.student_main import StudentMain


class GetStudentMarks(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help="Student roll number is required")

    @jwt_required
    def post(self):
        data = GetStudentMarks.parser.parse_args()

        student = StudentMain.find_by_roll_number(data['roll_no'])
        student_marks = {
            'roll_no': student.roll_no,
            'semester': student.current_sem,
            'subjects': []
        }
        if student:
            subject_code_list = Subjects.find_subject(student.discipline, student.current_sem)
            for subject in subject_code_list:
                subject_marks = StudentMarks.get_marks_all(subject, student.roll_no, student.current_sem)
                marks_details = {
                    'subject_name': Subjects.get_subject_name(subject),
                    'subject_code': subject_marks['subject_code'],
                    'cat': subject_marks['cat'],
                    'mid': subject_marks['mid'],
                    'end': subject_marks['end'],
                    'assignment': subject_marks['assignment'],
                    'attendance': subject_marks['attendance']
                }
                student_marks['subjects'].append(marks_details)
            return student_marks
        else:
            return {'message': 'No student with that roll number exists'}


class GetStudentMarksSemester(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help="Student roll number is required")

    @jwt_required
    def post(self, semester):
        data = GetStudentMarks.parser.parse_args()

        student = StudentMain.find_by_roll_number(data['roll_no'])
        student_marks = {
            'roll_no': student.roll_no,
            'semester': semester,
            'subjects': []
        }
        if student:
            subject_code_list = Subjects.find_subject(student.discipline, semester)
            for subject in subject_code_list:
                subject_marks = StudentMarks.get_marks_all(subject, student.roll_no, semester)
                marks_details = {
                    'subject_name': Subjects.get_subject_name(subject),
                    'subject_code': subject_marks['subject_code'],
                    'cat': subject_marks['cat'],
                    'mid': subject_marks['mid'],
                    'end': subject_marks['end'],
                    'assignment': subject_marks['assignment'],
                    'attendance': subject_marks['attendance']
                }
                student_marks['subjects'].append(marks_details)
            return student_marks
        else:
            return {'message': 'No student with that roll number exists'}