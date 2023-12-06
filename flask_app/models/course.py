from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models import user, registration
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")


class Course:
    db = 'creative_aging'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.requirements = data['requirements']
        self.course_img = data['course_img']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.start_time_hour = data['start_time_hour']
        self.start_time_min = data['start_time_min']
        self.start_time_ampm = data['start_time_ampm']
        self.end_time_hour = data['end_time_hour']
        self.end_time_min = data['end_time_min']
        self.end_time_ampm = data['end_time_ampm']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.students = []


    @classmethod
    def create_course(cls, form_data):
        # print("------FORM DATA-----", form_data)
        # if reference to the user is made here, a hidden input is not necessary in submit form. 
        if not cls.validate_create_course_form(form_data, files): return False
        form_data = cls.parse_course_data(form_data, files)
        query = """
                    INSERT INTO courses 
                        (title, 
                        description, 
                        price, 
                        requirements, 
                        course_img, 
                        start_date, 
                        end_date, 
                        start_time_hour, 
                        start_time_min, 
                        start_time_ampm, 
                        end_time_hour, 
                        end_time_min, 
                        end_time_ampm, 
                        user_id)
                    VALUES 
                        (%(title)s, 
                        %(description)s, 
                        %(price)s, 
                        %(requirements)s, 
                        %(course_img)s, 
                        %(start_date)s, 
                        %(end_date)s, 
                        %(start_time_hour)s, 
                        %(start_time_min)s, 
                        %(start_time_ampm)s, 
                        %(end_time_hour)s, 
                        %(end_time_min)s, 
                        %(end_time_ampm)s, 
                        %(user_id)s);
                """
        result = connectToMySQL(cls.db).query_db(query, form_data)
        # print("Create course method in model produced this result: ", result)
        return result

    @classmethod
    def get_all_courses_with_creator(cls):
        query = """
                    SELECT * FROM courses
                    LEFT JOIN users
                    ON courses.user_id = users.id
                    ORDER BY courses.created_at DESC;
                """
        results = connectToMySQL(cls.db).query_db(query)
        # print("REEEEEEEZZZZZZZULTZZZ:", results)
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
            # print("******* FROM THE MODEL - courses with their creator list: ", course_creator_list)
            return course_creator_list
        return results

    @classmethod
    def get_one_course_by_id_with_creator(cls, data):
        query = """
                    SELECT * FROM courses
                    LEFT JOIN users
                    ON courses.user_id = users.id
                    WHERE courses.id = %(id)s;
                """
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
    def update_course_by_id(cls, form_data, files='not needed'):
        if not cls.validate_create_course_form(form_data, files): return False
        form_data = cls.parse_course_data(form_data, files)
        if 'course_img' in files:
            query = """
                        UPDATE courses
                        SET 
                            title=%(title)s, 
                            description=%(description)s, 
                            price=%(price)s, 
                            requirements=%(requirements)s, 
                            course_img=%(course_img)s, 
                            start_date=%(start_date)s, 
                            end_date=%(end_date)s, 
                            start_time_hour=%(start_time_hour)s, 
                            start_time_min=%(start_time_min)s, 
                            start_time_ampm=%(start_time_ampm)s, 
                            end_time_hour=%(end_time_hour)s, 
                            end_time_min=%(end_time_min)s, 
                            end_time_ampm=%(end_time_ampm)s
                        WHERE id = %(id)s;
                    """
        else:
            query = """
                        UPDATE courses
                        SET 
                            title=%(title)s, 
                            description=%(description)s, 
                            price=%(price)s, 
                            requirements=%(requirements)s,
                            start_date=%(start_date)s, 
                            end_date=%(end_date)s, 
                            start_time_hour=%(start_time_hour)s, 
                            start_time_min=%(start_time_min)s, 
                            start_time_ampm=%(start_time_ampm)s, 
                            end_time_hour=%(end_time_hour)s, 
                            end_time_min=%(end_time_min)s, 
                            end_time_ampm=%(end_time_ampm)s
                        WHERE id = %(id)s;
                    """
        return connectToMySQL(cls.db).query_db(query, form_data) 

    @classmethod
    def delete_this_course_by_id(cls, data):
        query = """
                    DELETE FROM courses
                    WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_create_course_form(form_data, files):
        is_valid = True
        # print('_______>', form_data)
        # print('files ------->', files)
        if len(form_data['title']) > 0 and len(form_data['title']) <= 3:
            flash("title must be at least 4 characters.")
            is_valid = False
        if len(form_data['description']) > 700:
            flash("description must not exceed 700 characters.")
            is_valid = False
        if len(form_data['title']) <= 0 or len(form_data['description']) <= 0 or len(form_data['price']) <= 0:
            flash("All fields required.")
            is_valid = False
        if len(form_data['start_date']) <= 0 or len(form_data['end_date']) <= 0:
            flash("Dates need to be set.")
            is_valid = False
        if 'course_img' not in files:
            flash('No file part')
            is_valid = False
        if files != 'not needed':
            if files['course_img'].filename == '':
                flash('No selected file')
                is_valid = False
            if not (files['course_img'] and Course.allowed_file(files['course_img'].filename)):
                flash('File type not allowed')
                is_valid = False
        return is_valid

    @staticmethod
    def parse_course_data(data, files):
        data =  data.copy()
        requirements = request.form.getlist("requirements")
        requirements_string = '. '.join(requirements)
        data['requirements'] = requirements_string
        data['user_id'] = session['logged_in_user_id']
        if files!= 'not needed':
            if files['course_img'] and Course.allowed_file(files['course_img'].filename):
                filename = secure_filename(files['course_img'].filename)
                files['course_img'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data['course_img'] = filename
        return data

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
