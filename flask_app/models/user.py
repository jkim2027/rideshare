from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'ohana'
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def update_driver_to_rider(cls, data):
        query = "UPDATE rides SET driver_id=%(driver_id)s WHERE id=%(ride_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def cancel_ride(cls, data):
        query = "UPDATE rides SET driver_id=null WHERE id=%(ride_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results


    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address.", 'register')
            is_valid = False
        if user['conf_password'] != user['password']:
            flash("Passwords don't match.", 'register')
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash('Password should have at least one numeral', 'register')
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash('Password should have at least one uppercase letter', 'register')
            is_valid = False
        return is_valid