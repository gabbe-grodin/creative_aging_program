from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import user

class Course:
    db = 'creative_aging'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.requirements = data['requirements']
        self.img_url = data['img_url']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None


    @classmethod
    def create_course(cls, form_data):
        print("------FORM DATA-----", form_data)
        # course_data = {
        #     "title": form_data["title"],
        #     "description": form_data["description"],
        #     "user_id": form_data["user_id"]}
        # if reference to the user is made here, a hidden input is not necessary in submit form. 
        query = """INSERT INTO courses (title, description, price, requirements, img_url, start_date, end_date, start_time, end_time, user_id)
            VALUES (%(title)s, %(description)s, %(price)s, %(requirements)s, %(img_url)s, %(start_date)s, %(end_date)s, %(start_time)s, %(end_time)s, %(user_id)s)"""
        result = connectToMySQL(cls.db).query_db(query, form_data)
        print("Create course method in model produced this result: ", result)
        return result

    @classmethod
    def get_all_courses_with_creator(cls):
        query = """SELECT * FROM courses
            LEFT JOIN users
            ON courses.user_id = users.id;"""
        results = connectToMySQL(cls.db).query_db(query)
        print("REEEEEEEZZZZZZZULTZZZ:", results)
        if results: # assure loading dash won't crash app on first load before any courses are created:
            course_creator_list = []
            for row in results:
                one_course = cls(row)
                creator_data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "user_type": row["user_type"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
                one_course.creator = user.User(creator_data)
                course_creator_list.append(one_course)
            print("******* FROM THE MODEL - courses with their creator list: ", one_course)
            return course_creator_list
        return results

    @classmethod
    def get_one_course_by_id_with_creator(cls, data):
        query = """SELECT * FROM courses
            LEFT JOIN users
            ON courses.user_id = users.id
            WHERE courses.id = %(id)s"""
        result=connectToMySQL(cls.db).query_db(query, data)
        one_course = cls(result[0])
        # instance of course class and creator...
        for row in result:
            course_creator_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "user_type": row["user_type"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]}
        one_course.creator = user.User(course_creator_data)
        if one_course:
            return one_course
        else:
            return False

    @classmethod
    def update_course_by_id(cls, data):
        query = """UPDATE courses
                SET title=%(title)s, description=%(description)s, price=%(price)s, requirements=%(requirements)s, img_url=%(img_url)s, start_date=%(start_date)s, end_date=%(end_date)s, start_time=%(start_time)s, end_time=%(end_time)s
                WHERE id = %(id)s"""
        return connectToMySQL(cls.db).query_db(query, data) 

    @classmethod
    def delete_this_course_by_id(cls, data):
        query = """DELETE FROM courses
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_create_course_form(form_data):
        is_valid = True
        if len(form_data['title']) > 0 and len(form_data['title']) <= 3:
            flash("title must be at least 4 characters.")
            is_valid = False
        if len(form_data['description']) > 500:
            flash("description must not exceed 500 characters.")
            is_valid = False
        if len(form_data['title']) <= 0 or len(form_data['description']) <= 0 or len(form_data['price']) <= 0:
            flash("All fields required.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit_course_form(form_data):
        is_valid = True
        if len(form_data['title']) > 0 and len(form_data['title']) <= 3:
            flash("title must be at least 4 characters.")
            is_valid = False
        if len(form_data['description']) > 500:
            flash("description must not exceed 500 characters.")
            is_valid = False
        if len(form_data['title']) <= 0 or len(form_data['description']) <= 0 or len(form_data['price']) <= 0:
            flash("All fields required.")
            is_valid = False
        return is_valid

