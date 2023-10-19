from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.course import Course
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#! login-registration forms
@app.route('/')
def index():
    return render_template('index.html')

#! register
@app.route('/user/create', methods=['POST'])
def register_new_user():
    if not User.validate_registration_form(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "user_type": request.form['user_type'],
        "email": request.form['email'],
        "password": pw_hash}
    logged_in_user_id = User.create_user(data)
    # stores user in session:
    session['logged_in_user_id'] = logged_in_user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['user_type'] = request.form['user_type']
    session['email'] = request.form['email']
    print("-------", session)
    return redirect('/dashboard')

#! login
@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    logged_in_user_id = User.get_one_user_by_email(request.form)
    if not logged_in_user_id:
        flash("Invalid email/password.")
        return redirect('/')
    if not bcrypt.check_password_hash(logged_in_user_id.password, request.form['password']):
        flash("Invalid email/password.")
        return redirect('/')
    session['logged_in_user_id'] = logged_in_user_id.id
    session['first_name'] = logged_in_user_id.first_name
    session['last_name'] = logged_in_user_id.last_name
    session['email'] = logged_in_user_id.email
    return redirect('/dashboard')

#! dashboard
@app.route('/dashboard')
def dashboard():
    # protect route if user not logged in:
    if 'logged_in_user_id' not in session:
        flash("Please log in.")
        return redirect('/')
    all_courses = Course.get_all_courses_with_creator()
    return render_template("dash.html", all_courses=all_courses)

#! user account
@app.route('/user/<int:logged_in_user_id>')
def user_account(logged_in_user_id):
    data = {"id": session['logged_in_user_id']}
    # protect route if user not logged in:
    if 'logged_in_user_id' not in session:
        flash("Please log in.")
        return redirect('/')
    # user = User.get_one_user_by_id(data)
    creator = User.get_one_user_by_id_with_courses(data)
    print("CREATOR-------", creator)
    return render_template("account.html", creator=creator)

#! logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



# #! update post
# @app.route('/user/update', methods=['POST'])
# def user_update():
#     if not User.validate_user_update_form(request.form):
#         return redirect(f'/user/{session["logged_in_user_id"]}')
#     # data={"first_name": request.form['first_name'],
#     #     "last_name": request.form['last_name'],
#     #     "email": request.form['email']}
#     User.user_update(request.form)
#     return redirect(f'/user/{session["logged_in_user_id"]}')
