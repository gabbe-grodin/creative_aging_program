from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.course import Course
from flask_app.models.user import User
from flask_app.models.registration import Registration
from werkzeug.utils import secure_filename
from flask_app import app
import os

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

#! add form
@app.route('/course/new')
def add_course_form():
    if 'logged_in_user_id' not in session: return redirect('/')
    if session['user_type'] == 'student': return redirect('/')
    return render_template('add_one.html')

#! the following code is from https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#! create course
@app.route('/course/create', methods=['POST'])
def create_course():
    if 'logged_in_user_id' not in session: return redirect('/')
    if Course.create_course(request.form, request.files): # moved validations to helper function in model and beginning skinny controller fat model setup  plus added request.files
        return redirect(f"/teacher/{session['logged_in_user_id']}")
    return redirect('/course/new')

#! view one
@app.route('/course/<int:id>')
def view_one_course_w_creator(id):
    if 'logged_in_user_id' not in session: return redirect('/')
    data = {"id":id}
    course = Course.get_one_course_by_id_with_creator(id)
    user = session['logged_in_user_id']
    return render_template('view_one.html', course = course, user = user)

#! edit course form
@app.route('/course/edit/<int:id>')
def course_edit(id):
    if 'logged_in_user_id' not in session: return redirect('/')
    if session['user_type'] == 'student':
        return redirect('/')
    course = Course.get_one_course_by_id_with_creator(id)
    return render_template('edit_one.html', course = course)

#! update course post
@app.route('/course/update', methods=['POST'])
def course_update():
    if session['user_type' == 'student']: return redirect('/')
    if request.files: files = request.files
    else: files = 'not needed'
    if Course.update_course_by_id(request.form, files):
        return redirect(f'/course/{request.form["id"]}')
    return redirect(f'/course/edit/{request.form["id"]}')

#! delete
@app.route('/delete/<int:id>')
def delete(id):
    data = {"id":id}
    Course.delete_this_course_by_id(data)
    return redirect('/dashboard')

#! upload file (move to diff/new controller?)
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return