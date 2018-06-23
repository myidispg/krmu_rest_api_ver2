import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class EventsModel:

    def __init__(self, event_code, event_name, event_description, start_date, end_date, start_time, end_time,
                 venue, file_path, organiser_code, new_interest):
        self.event_code = event_code
        self.event_name = event_name
        self.event_description = event_description
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.venue = venue
        self.file_path = file_path
        self.organiser_code = organiser_code
        self.new_interest = new_interest

    @classmethod
    def find_by_event_code(cls, event_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * from events WHERE event_code = ?"
        result = cursor.execute(query, (event_code,))

        row = result.fetchone()
        if row is not None:
            event = cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                        row[10])
            connection.close()
            return event

        connection.close()
        return None

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        cursor.execute(query, (self.event_code, self.event_name, self.event_description, self.start_date,
                               self.end_date, self.start_time, self.end_time, self.venue,
                               self.file_path, self.organiser_code,self.new_interest))

        connection.commit()
        connection.close()

    @staticmethod
    def get_counter(counter):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT event_code FROM events ORDER BY event_code"
        result = cursor.execute(query)

        rows = result.fetchall()
        final_counter = counter

        for row in rows:
            row = "".join(row)
            _list = row.split('-')
            row_counter = int(_list[len(_list)-1])
            if row_counter == final_counter:
                final_counter += 1

        connection.close()
        return final_counter

    @classmethod
    def get_all_events(cls):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM events"
        result = cursor.execute(query)

        rows = result.fetchall()
        events_list = []
        for row in rows:
            event = cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                        row[9], row[10])
            events_list.append(event)
        connection.close()
        return events_list

    def json(self):
        return {
            'event_code': self.event_code,
            'event_name': self.event_name,
            'event_description': self.event_description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'venue': self.venue,
            'organiser_code': self.organiser_code,
            'new_interest': self.new_interest
        }

    @staticmethod
    def change_new_interest(event_code, interest):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "UPDATE events SET new_interest = ? where event_code = ?"
        cursor.execute(query, (interest, event_code,))

        connection.commit()
        connection.close()



