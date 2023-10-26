import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

load_dotenv()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY
