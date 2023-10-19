from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY
