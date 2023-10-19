from flask import render_template, redirect, request, session, flash
from flask_app.models.course import Course
from flask_app.models.user import User
from flask_app import app

#! add form
@app.route('/course/new')
def add_course_form():
    return render_template('add_one.html')
    # data = {"id": session["logged_in_user_id"],
    #         "first_name": session["first_name"],
    #         "last_name": session["last_name"]}
    # if session['logged_in_user_id']:
    #     user = User.get_one_user_by_id(data)
    #     return render_template('add_one.html', user = user)
    # else:
    #     return redirect('/')


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
            "start_time": request.form['start_time'],
            "end_time": request.form['end_time'],
            "user_id": session['logged_in_user_id']}
    print ("* * *    printing ****** : ", session)
    Course.create_course(data)
    print("Ready to reroute!!!!!!!!!!")
    return redirect(f"/user/{session['logged_in_user_id']}")

#! view one
@app.route('/course/<int:id>')
def view_one_course_w_creator(id):
    data = {"id":id}
    course = Course.get_one_course_by_id_with_creator(data)
    user_data = {"logged_in_user_id":session['logged_in_user_id']}
    # logged_in_user = User.get_one_user_by_id(user_data)
    # return render_template('view_one.html', course = course, logged_in_user = logged_in_user)
    return render_template('view_one.html', course = course)

#! edit course form
#! call validation method
@app.route('/course/edit/<int:id>')
def course_edit(id):
    data = {"id":id}
    course = Course.get_one_course_by_id_with_creator(data)
    return render_template('edit_one.html', course = course)

@app.route('/course/update', methods=['POST'])
def course_update():
    print("PPPPRRRRRRIIIINNNNTTTT-----", request.form)
    data = {"id":id}
    if not Course.validate_edit_course_form(request.form):
        return redirect(f'/course/edit/{request.form["id"]}')
    # data = {"species": request.form['species'],
    #         "location": request.form['location'],
    #         "date_planted": request.form['date_planted'],
    #         "reason": request.form['reason']}
    Course.update_course_by_id(request.form)
    return redirect(f'/course/{request.form["id"]}')



#! delete
@app.route('/delete/<int:id>')
def delete(id):
    data = {"id":id}
    Course.delete_this_course_by_id(data)
    return redirect(f'/user/{session["logged_in_user_id"]}')