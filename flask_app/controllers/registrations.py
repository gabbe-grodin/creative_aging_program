from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models.course import Course
from flask_app.models.user import User
from flask_app.models.registration import Registration
from werkzeug.utils import secure_filename
import os


# form - student course signup
@app.route('/registration/new/<int:id>/<int:course_id>')
def user_course_signup_form(id, course_id):
    data = {"id": course_id} 
    print("DATA***********", data)
    user = session['logged_in_user_id']
    course = Course.get_one_course_by_id_with_creator(data)
    print("course.........", course)
    return render_template('student_signup.html', course = course, user=user)

# create course reg/ student signs up for a class
@app.route('/sign_up', methods=['POST'])
def user_registers_for_course():
    print("routing success !!!!!!!!!!!!----------")
    # print("id----------",id)
    data = {
        "user_id": session['logged_in_user_id'], # comes from session
        "course_id": request.form['course_id']}
    print("data > > > > > > > > > > > >",data)
    Registration.user_registers_for_course(data)
    return redirect(f'/course/{data["course_id"]}')