from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models.course import Course
from flask_app.models.user import User
from flask_app.models.registration import Registration
from werkzeug.utils import secure_filename
import os


# form
@app.route('/registration/new/<int:id>')
def user_course_signup_form(id):
    return render_template('student_signup.html')

# create course reg/ student signs up for a class
@app.route('/sign_up', methods=['POST'])
def user_registers_for_course(id):
    print("routing success !!!!!!!!!!!!----------")
    # print("id----------",id)
    # print("session----------",session)
    data = {
        "user_id": session['logged_in_user_id'], # comes from session
        "course_id": id}
    registration.Registration.user_registers_for_course(data)
    return redirect(f'/course/{data["id"]}')