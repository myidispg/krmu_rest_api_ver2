import os

from flask_restful import Resource, reqparse

from models.daily_attendance import DailyAttendanceModel


class GetDailyAttendanceStudent(Resource):

    def get(self, roll_no, subject_code):

        daily_attendance = {
            'roll_no': roll_no,
            'subject_code': subject_code,
            'daily_attendance': DailyAttendanceModel.get_daily_attendance_by_roll_sub_code(roll_no, subject_code)
        }

        return daily_attendance
