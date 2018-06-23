from flask import request
from flask_restful import Resource, reqparse

from models.events import EventsModel
from models.events_interested import EventsInterestedModel


class AddEventInterest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('event_code', type=str, required=True, help='event_code is required')
    parser.add_argument('roll_no', type=str, required=True, help='student roll_no is required')

    def post(self):
        data = self.parser.parse_args()

        event_interest = EventsInterestedModel(data['event_code'], data['roll_no'])
        event_interest.save_to_db()
        EventsModel.change_new_interest(data['event_code'], 'Y')

        return {
            'message': 'Your interest has been recorded to the database. The event organiser will '
                       'be notified of the same'
        }


class ShowInterestedOrganiser(Resource):

    def get(self, event_code):
        interested_list = EventsInterestedModel.get_all_interested_event_code(event_code)

        EventsModel.change_new_interest(event_code, 'N')
        return {
            'interested_list': interested_list
        }


class ShowInterestedStudent(Resource):

    def get(self, roll_no):
        interested_list = EventsInterestedModel.get_all_interested_roll_no(roll_no)

        for interest in interested_list:
            event = EventsModel.find_by_event_code(interest['event_code'])
            interest['event_name'] = event.event_name
            interest['start_date'] = event.start_date
            interest['end_date'] = event.end_time

        return {
            'interested_list': interested_list
        }

