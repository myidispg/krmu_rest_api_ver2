import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class EventsInterestedModel:

    def __init__(self, event_code, roll_no):
        self.event_code = event_code
        self.roll_no = roll_no

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO event_interested values(?,?)"
        cursor.execute(query, (self.event_code, self.roll_no,))

        connection.commit()
        connection.close()

