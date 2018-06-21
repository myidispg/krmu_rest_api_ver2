import os

from flask import request, send_file
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.security import safe_str_cmp

from models.daily_attendance import DailyAttendanceModel


class DailyAttendanceUpdateResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help='roll number is required')
    parser.add_argument('subject_code', type=str, required=True, help='subject_code is required')
    parser.add_argument('semester', type=str, required=True, help='semester is required')
    parser.add_argument('date', type=str, required=True, help='date is required')
    parser.add_argument('day', type=str, required=True, help='day is required')
    parser.add_argument('status', type=str, required=True, help='student status is required')

    def post(self):
        data = self.parser.parse_args()

        daily_attendance = DailyAttendanceModel(data['roll_no'], data['subject_code'], data['semester'],
                                                data['date'], data['day'], data['status'])
        daily_attendance.save_to_db()
        return {
            'message': 'Attendance updated successfully!'
        }