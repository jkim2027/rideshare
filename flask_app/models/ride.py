from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Ride:
    DB = 'ohana'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.destination = db_data['destination']
        self.pickup = db_data['pickup']
        self.ride_date = db_data['ride_date']
        self.details = db_data['details']
        self.driver_id = db_data['driver_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = None
        self.driver = None

    @classmethod
    def new_ride(cls, data):
        query = "INSERT INTO rides (driver_id, user_id, destination, pickup, ride_date, details, created_at, updated_at) VALUES (%(driver_id)s, %(user_id)s, %(destination)s, %(pickup)s, %(ride_date)s, %(details)s, NOW(), NOW())"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM rides JOIN users ON users.id = rides.user_id LEFT JOIN users as drivers ON rides.driver_id = drivers.id"
        results = connectToMySQL(cls.DB).query_db(query)
        all_rides = []
        for ride in results:
            each_user = User({
                'id': ride['user_id'],
                'email': ride['email'],
                'first_name': ride['first_name'],
                'last_name': ride['last_name'],
                'password': ride['password'],
                'created_at': ride['users.created_at'],
                'updated_at': ride['users.updated_at']
            })
            new_ride = cls(ride)
            each_driver = User({
                'id': ride['driver_id'],
                'email': ride['drivers.email'],
                'first_name': ride['drivers.first_name'],
                'last_name': ride['drivers.last_name'],
                'password': ride['drivers.password'],
                'created_at': ride['drivers.created_at'],
                'updated_at': ride['drivers.updated_at']
            })
            new_ride.user = each_user
            new_ride.driver = each_driver
            all_rides.append(new_ride)
        return all_rides
    
    @classmethod
    def get_one_ride(cls, ride_id):
        query = "SELECT * FROM rides JOIN users ON users.id = rides.user_id JOIN users as drivers ON rides.driver_id = drivers.id WHERE rides.id=%(id)s"
        data = {'id': ride_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        ride = cls(results[0])
        user_data = {
            'id': results[0]['users.id'],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            'email': results[0]['email'],
            'password': results[0]['password'],
            "created_at": results[0]["users.created_at"],
            'updated_at': results[0]['users.updated_at']
        }
        driver_data = {
            'id': results[0]['drivers.id'],
            "first_name": results[0]["drivers.first_name"],
            "last_name": results[0]["drivers.last_name"],
            'email': results[0]['drivers.email'],
            'password': results[0]['drivers.password'],
            "created_at": results[0]["drivers.created_at"],
            'updated_at': results[0]['drivers.updated_at']
        }
        user = User(user_data)
        driver = User(driver_data)
        ride.user = user
        ride.driver = driver
        return ride
    
    @classmethod
    def delete_ride(cls, ride_id):
        query = "DELETE FROM rides WHERE id=%(id)s"
        data = {'id': ride_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def update_ride(cls, data):
        query = "UPDATE rides SET pickup = %(pickup)s, details = %(details)s WHERE id=%(ride_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @staticmethod
    def validate_ride(ride):
        is_valid = True
        if len(ride['destination']) <= 0 and len(ride['pickup']) <= 0 and len(ride['ride_date']) <= 0 and len(ride['details']) < 0:
            flash("All fields required.", 'ride')
            is_valid = False
        if len(ride['destination']) < 3:
            flash("Destination must be at least 3 characters.","ride")
            is_valid = False
        if len(ride['pickup']) < 3:
            flash("Pick-up location must be at least 3 characters.","ride")
            is_valid = False
        if len(ride['ride_date']) <= 0:
            flash("Date must be given.","ride")
            is_valid = False
        if len(ride['details']) < 10:
            flash("Details must be at least 10 characters.", "ride")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_update(ride):
        is_valid = True
        if len(ride['pickup']) <= 0 and len(ride['details']) <= 0:
            flash("All fields required.", 'update')
            is_valid = False
        if len(ride['pickup']) < 3:
            flash("Pick-up location must be at least 3 characters.","update")
            is_valid = False
        if len(ride['details']) < 10:
            flash("Details must be at least 10 characters.", "update")
            is_valid = False
        return is_valid