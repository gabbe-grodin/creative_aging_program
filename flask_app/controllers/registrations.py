from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models.course import Course
from flask_app.models.user import User
from flask_app.models.registration import Registration
from werkzeug.utils import secure_filename
import os


# create
@app.route('/registration/create/<int:id>', methods=['POST'])
def user_registers_for_course(id):
    # print("id----------",id)
    # print("session----------",session)
    data = {
        "user_id": session['logged_in_user_id'], # comes from session
        "course_id": id}
    registration.Registration.user_registers_for_course(data)
    return redirect(f'/course/{data["id"]}')



# @app.route('/author/add/favorite', methods=['POST'])
# def make_association_from_one_author_page():
#     data = {
#         "author_id": request.form['author'], # comes from name in form
#         "book_id": request.form['book']}
#     print("*************DATA***********",data)
#     author.Author.add_a_favorite(data)
#     return redirect(f"/author/{request.form['author']}")