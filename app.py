import os
from flask import Flask, render_template, session
from utils.db import get_db
from dotenv import load_dotenv

load_dotenv()


MONGO_URI = os.environ.get('MONGO_URI')
SECRET_KEY = os.environ.get('SECRET_KEY', 'replace-with-secure-key')


app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = SECRET_KEY