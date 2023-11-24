from flask_app import app
from flask_app.controllers import users, courses, registrations

if __name__== "__main__":
    app.run(debug=True, host="localhost", port=8000)