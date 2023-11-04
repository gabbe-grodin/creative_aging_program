from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import user, course

class Registration:
    db = 'creative aging'
    def __init__(self, data):
        self.user_id = data['user_id']
        self.course_id = data['course_id']

    @classmethod
    def user_registers_for_course(cls,data):
        print("DDDAAAATTTAAAA:::::", data)
        query = """
            INSERT INTO registrations
            (user_id, course_id)
            VALUES (%(user_id)s, %(course_id)s);"""
        result = connectToMySQL(cls.db).query_db(query, data)
        print("RRRRRRREEEEEEEEEEEESSSSSUUUULLLLT:",result)
        return result