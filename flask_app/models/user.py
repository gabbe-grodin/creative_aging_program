from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import course, registration
bcrypt = Bcrypt(app)
import re

class User:
    db = 'creative_aging'
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.user_type=data['user_type']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.courses = [] # created
        self.registrations = [] # student sign-ups

    @classmethod
    def create_user(cls,data):
        query="""
            INSERT INTO users (first_name, last_name, user_type, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(user_type)s, %(email)s, %(password)s);"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_all_users(cls):
        query = """
            SELECT * 
            FROM users;"""
        all_users =  connectToMySQL(cls.db).query_db(query)
        return all_users

    @staticmethod
    def validate_registration_form(form_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        if len(form_data['first_name']) > 0 and len(form_data['first_name']) <= 1:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(form_data['first_name']) <= 0:
            flash("Cannot leave first name field blank. ")
            is_valid = False
        if len(form_data['last_name']) > 0 and len(form_data['last_name']) <= 1:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if 'user_type' not in form_data:
            flash("Must state your role with the project.")
            is_valid = False
        if len(form_data['last_name']) <= 0:
            flash("Cannot leave last name field blank.")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']) and len(form_data['email']) > 0:
            flash("Email must be in correct format.")
            is_valid = False
        if len(form_data['email']) <= 0:
            flash("Cannot leave email field blank.")
            is_valid = False
        if User.get_one_user_by_email(form_data):
        # if User.get_one_user_by_email(form_data['email']):
            flash("Email is already in our system. Please try again.")
            is_valid = False
        if len(form_data['password']) > 0 and len(form_data['password']) <= 7:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if len(form_data['password']) <= 0:
            flash("Cannot leave password field blank.")
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid
    
    @staticmethod
    def login_user(data):
        this_user = User.get_one_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['logged_in_user_id'] = this_user.id
                session['full_name'] = f"{this_user.first_name} {this_user.last_name}"
                return True
            else:
                flash("Your login failed.") # keep vague for security
                return False
        else:
            flash("Your login failed.")
            return False

    @classmethod
    def get_one_user_by_email(cls, email):
        print("EMAIL:", email)
        query = """SELECT * FROM users
            WHERE email = %(email)s"""
        result = connectToMySQL(cls.db).query_db(query, email)
        print("RESULT OF QUERY TO CHECK IF EMAIL EXISTS ALREADY: ", result)
        if result: # if email (result) exists
            one_user = cls(result[0]) # create class instantiate of user and return
            return one_user
        else:
            print("User/email not yet in db.")
            return False

    @classmethod
    def get_one_user_by_id(cls, id):
        query = """SELECT * FROM users
            WHERE id = %(id)s"""
        data = {"id": id}
        result=connectToMySQL(cls.db).query_db(query, data)
        if result:
            one_user = cls(result[0])
            return one_user
        return False

    @classmethod
    def get_one_user_by_id_with_courses(cls,data):
        query="""
            SELECT * 
            FROM users
            LEFT JOIN courses
            ON users.id = courses.user_id
            WHERE users.id = %(id)s
            ORDER BY courses.created_at DESC;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        this_user = cls(results[0]) # here we made a user object
        # print(this_user)
        for row in results:
            if row['courses.id'] != None: # This conditional prevents users without any courses from creating a null instance of a course and printing 'None'
                course_data = {
                    "id": row["courses.id"],
                    "title": row["title"],
                    "description": row["description"],
                    "price": row["price"],
                    "requirements": row["requirements"],
                    "course_img": row["course_img"],
                    "start_date": row["start_date"],
                    "end_date": row["end_date"],
                    "start_time_hour": row["start_time_hour"],
                    "start_time_min": row["start_time_min"],
                    "start_time_ampm": row["start_time_ampm"],
                    "end_time_hour": row["end_time_hour"],
                    "end_time_min": row["end_time_min"],
                    "end_time_ampm": row["end_time_ampm"],
                    "created_at": row['courses.created_at'],
                    "updated_at": row['courses.updated_at'],
                    "user_id":row['user_id']}
                courses = this_user.courses.append(course.Course(course_data))
        return this_user

    @classmethod
    def user_update(cls, data):
        query = """
                UPDATE users
                SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s
                WHERE id = %(logged_in_user_id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = """DELETE FROM users WHERE id = %(id)s"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_user_update_form(form_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        if len(form_data['first_name']) > 0 and len(form_data['first_name']) <= 2:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(form_data['first_name']) <= 0:
            flash("Cannot leave first name field blank. ")
            is_valid = False
        if len(form_data['last_name']) > 0 and len(form_data['last_name']) <= 2:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if len(form_data['last_name']) <= 0:
            flash("Cannot leave last name field blank.")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']) and len(form_data['email']) > 0:
            flash("Email must be in correct format.")
            is_valid = False
        if len(form_data['email']) <= 0:
            flash("Cannot leave email field blank.")
            is_valid = False
        return is_valid