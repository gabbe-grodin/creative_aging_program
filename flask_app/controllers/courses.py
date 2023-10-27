from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.course import Course
from flask_app.models.user import User
from werkzeug.utils import secure_filename
from flask_app import app
# from dotenv import load_dotenv
# from pathlib import Path
# from dotenv import ALLOWED_EXTENSIONS
import os

# load_dotenv()
# dotenv_path = Path('/.env')
# load_dotenv(dotenv_path=dotenv_path)

# why are below lines necessary in [app breaks without] both this file and __init__.py?
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#! add form
@app.route('/course/new')
def add_course_form():
    return render_template('add_one.html')

#! the following code is from https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#! create course
@app.route('/course/create', methods=['POST'])
def create_course():
    if not Course.validate_create_course_form(request.form):
        return redirect('/course/new')
    #! code from flask docs for uploading file: 
    if request.method == 'POST':
        print('=======   request.files:',request.files)
        # check if the post request has the file part
        if 'course_img' not in request.files:
            flash('No file part')
            return redirect(request.url)
        course_img = request.files['course_img']
        print("========     course_img is now equal to ",course_img)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if course_img.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if course_img and allowed_file(course_img.filename):
            filename = secure_filename(course_img.filename)
            course_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            #! end block from flask documentation
    session["user_id"] = request.form['logged_in_user_id']

    data = {"title": request.form['title'],
            "description": request.form['description'],
            "price": request.form['price'],
            "requirements": request.form['requirements'],
            "course_img": filename,
            "start_date": request.form['start_date'],
            "end_date": request.form['end_date'],
            "start_time_hour": request.form['start_time_hour'],
            "start_time_min": request.form['start_time_min'],
            "start_time_ampm": request.form['start_time_ampm'],
            "end_time_hour": request.form['end_time_hour'],
            "end_time_min": request.form['end_time_min'],
            "end_time_ampm": request.form['end_time_ampm'],
            "user_id": session['logged_in_user_id']}
    # data2 = request.form.copy()
    # data2['logged_in_user_id'] = session['logged_in_user_id']
    # data2["image_url"] =  request.form["course_img"]
    # print("data2 data2 data2 data2 at course_img..........",data2["course_img"])
    # filename = data2["course_img"]
    # print(("****** data2 ========== ",data2))
    # print("****** filename ========== ",filename)
    # print("****** session ========== ",session)
    Course.create_course(data)
    return redirect(f"/user/{session['logged_in_user_id']}")



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


#! view one
@app.route('/course/<int:id>')
def view_one_course_w_creator(id):
    data = {"id":id}
    course = Course.get_one_course_by_id_with_creator(data)
    return render_template('view_one.html', course = course)

#! edit course form
@app.route('/course/edit/<int:id>')
def course_edit(id):
    data = {"id":id}
    course = Course.get_one_course_by_id_with_creator(data)
    return render_template('edit_one.html', course = course)

#! update course post
@app.route('/course/update', methods=['POST'])
def course_update():
    data = {"id":id}
    if not Course.validate_edit_course_form(request.form):
        return redirect(f'/course/edit/{request.form["id"]}')
    Course.update_course_by_id(request.form)
    return redirect(f'/course/{request.form["id"]}')

#! delete
@app.route('/delete/<int:id>')
def delete(id):
    data = {"id":id}
    Course.delete_this_course_by_id(data)
    return redirect(f'/user/{session["logged_in_user_id"]}')