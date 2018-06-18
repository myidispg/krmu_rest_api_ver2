import os

import werkzeug
from flask import send_file
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename

from models.events import EventsModel


class EventsRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('event_name', type=str, required=True, help='event_name is required')
    parser.add_argument('event_description', type=str, required=False)
    parser.add_argument('start_date', type=str, required=False)
    parser.add_argument('end_date', type=str, required=False)
    parser.add_argument('start_time', type=str, required=False)
    parser.add_argument('end_time', type=str, required=False)
    parser.add_argument('venue', type=str, required=False)
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, required=False,
                        help='file is required', location='files')

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'ppt', 'docx', 'jpg', 'png', 'jpeg'])
    UPLOAD_FOLDER_SUBMISSIONS_PATH = "C:\KRMU_App\database\events"

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def post(self):
        data = self.parser.parse_args()

        counter = str(EventsModel.get_counter(1))
        event_code = "event-" + counter

        file = data['file']
        if file is not None:
            if file.filename == '':
                return {'message': 'The uploaded file has no filename'}
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_name_list = filename.split('.')
                new_file_name = os.path.normpath(os.path.join(self.UPLOAD_FOLDER_SUBMISSIONS_PATH, event_code + '.'
                                                              + file_name_list[len(file_name_list)-1]))
                file.save(new_file_name)
                event = EventsModel(event_code, data['event_name'], data['event_description'], data['start_date'],
                                    data['end_date'], data['start_time'], data['end_time'], data['venue'],
                                    new_file_name)
                event.save_to_db()

        else:
            event = EventsModel(event_code, data['event_name'], data['event_description'], data['start_date'],
                                data['end_date'], data['start_time'], data['end_time'], data['venue'], None)
            event.save_to_db()
        return {
           'message': 'Event registration successful'
        }, 201


class EventFile(Resource):

    def get(self, event_code):
        event = EventsModel.find_by_event_code(event_code)

        filename = event.file_path
        if filename is None:
            return {'message': 'this event has no file'}
        else:
            file_list = filename.split('.')
            file_dictionary = {
                'filename': filename
            }
            return send_file(file_dictionary['filename'])


class EventSingle(Resource):

    def get(self, event_code):
        event = EventsModel.find_by_event_code(event_code)

        return event.json()
