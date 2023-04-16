from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.ride import Ride

class Message:
    DB = 'ohana'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.message = db_data['message']
        self.ride_id = db_data['ride_id']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = None
        self.ride = None

    @classmethod
    def post_message(cls, data):
        query = "INSERT INTO messages(message, ride_id, user_id, created_at, updated_at) VALUES (%(message)s, %(ride_id)s, %(user_id)s, NOW(), NOW())"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_message(cls, ride_id):
        query = """SELECT * FROM messages
            JOIN rides ON rides.id=messages.ride_id
            JOIN users ON messages.user_id=users.id
            WHERE rides.id=%(id)s"""
        data = {'id': ride_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        all_messages = []
        for message in results:
            each_message = cls(message)
            each_ride = Ride({
                'id': message['ride_id'],
                'destination': message['destination'],
                'pickup':message['pickup'],
                'ride_date':message['ride_date'],
                'details':message['details'],
                'driver_id': message['driver_id'],
                'created_at': message['rides.created_at'],
                'updated_at': message['rides.updated_at']
                })
            each_user = User({
                'id': message['user_id'],
                "first_name": message["first_name"],
                "last_name": message["last_name"],
                'email': message['email'],
                'password': message['password'],
                "created_at": message["users.created_at"],
                'updated_at': message['users.updated_at']
                })
            each_message.ride = each_ride
            each_message.user = each_user
            all_messages.append(each_message)
        return all_messages