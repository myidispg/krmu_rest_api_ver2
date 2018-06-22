from flask import request
from flask_restful import Resource, reqparse

from models.events_interested import EventsInterestedModel


class AddEventInterest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('event_code', type=str, required=True, help='event_code is required')
    parser.add_argument('roll_no', type=str, required=True, help='student roll_no is required')

    def post(self):
        data = self.parser.parse_args()

        event_interest = EventsInterestedModel(data['event_code'], data['roll_no'])
        event_interest.save_to_db()

        return {
            'message': 'Your interest has been recorded to the database. The event organiser will '
                       'be notified of the same'
        }
