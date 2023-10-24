from flask import render_template, redirect, request, session, flash
from flask_app.models.course import Course
from flask_app.models.user import User
from flask_app import app




#! add form
@app.route('/course/new')
def add_course_form():
    return render_template('add_one.html')


#! create course
@app.route('/course/create', methods=['POST'])
def create_course():
    if not Course.validate_create_course_form(request.form):
        return redirect('/course/new')
    session["user_id"] = request.form['logged_in_user_id']
    data = {"title": request.form['title'],
            "description": request.form['description'],
            "price": request.form['price'],
            "requirements": request.form['requirements'],
            "img_url": request.form['img_url'],
            "start_date": request.form['start_date'],
            "end_date": request.form['end_date'],
            "start_time_hour": request.form['start_time_hour'],
            "start_time_min": request.form['start_time_min'],
            "start_time_ampm": request.form['start_time_ampm'],
            "end_time_hour": request.form['end_time_hour'],
            "end_time_min": request.form['end_time_min'],
            "end_time_ampm": request.form['end_time_ampm'],
            "user_id": session['logged_in_user_id']}
    Course.create_course(data)
    return redirect(f"/user/{session['logged_in_user_id']}")

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
    print("PPPPRRRRRRIIIINNNNTTTT-----", request.form)
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