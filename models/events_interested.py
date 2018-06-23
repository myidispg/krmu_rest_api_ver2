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

    @staticmethod
    def get_all_interested_event_code(event_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * from event_interested WHERE event_code = ? "
        result = cursor.execute(query, (event_code,))

        rows = result.fetchall()
        interested_list = []
        for row in rows:
            dictionary = {
                'event_code': row[0],
                'roll_no': row[1]
            }
            interested_list.append(dictionary)

        connection.close()
        return interested_list

    @staticmethod
    def get_all_interested_roll_no(roll_no):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM event_interested where roll_no = ?"
        result = cursor.execute(query, (roll_no,))

        rows = result.fetchall()
        interested_list = []
        for row in rows:
            dictionary = {
                'event_code': row[0],
                'roll_no': row[1]
            }
            interested_list.append(dictionary)

        connection.close()
        return interested_list
