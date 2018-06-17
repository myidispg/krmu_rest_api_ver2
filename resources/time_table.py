from flask_restful import Resource, reqparse

from models.time_table import TimeTableModel
from models.subjects import Subjects


class TimeTableStudent(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("discipline", type=str, required=True, help='discipline is required')
    parser.add_argument('semester', type=str, required=True, help='semester is required')

    def post(self):
        data = self.parser.parse_args()

        subject_code_list = Subjects.find_subject(data['discipline'], data['semester'])
        time_table_outer = {
            'subject_list': []
        }

        for subject in subject_code_list:
            subject_object = Subjects.get_subject_object(subject)
            time_table_list = TimeTableModel.get_all_by_subject_code(subject)
            dictionary = {
                'subject_code': subject_object.subject_code,
                'subject_name': subject_object.subject_name,
                'time_table': []
            }
            for time_table in time_table_list:
                inner_dictionary = {
                    'day': time_table.day,
                    'start_time': time_table.start_time,
                    'end_time': time_table.end_time,
                    'teacher_code': time_table.teacher_code
                }
                dictionary['time_table'].append(inner_dictionary)
            time_table_outer['subject_list'].append(dictionary)

        return time_table_outer


class TimeTableTeacher(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('teacher_code', type=str, required=True, help='teacher_code is required')

    def post(self):
        data = self.parser.parse_args()

        time_table_outer = {
            'subjects': []
        }
        time_table_list = TimeTableModel.get_all_by_teacher_code(data['teacher_code'])
        for time_table in time_table_list:
            subject_name = Subjects.get_subject_name(time_table.subject_code)
            dictionary = {
                'subject_code': time_table.subject_code,
                'subject_name': subject_name,
                'day': time_table.day,
                'start_time': time_table.start_time,
                'end_time': time_table.end_time,
            }
            time_table_outer['subjects'].append(dictionary)
        return time_table_outer







