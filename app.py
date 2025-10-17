import os
from flask import Flask, render_template, session
from utils.db import get_db
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.environ.get('MONGO_URI')
SECRET_KEY = os.environ.get('SECRET_KEY', 'replace-with-secure-key')


app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = SECRET_KEY


# Initialize DB helper (lazy connect inside utils/db.py)
get_db(MONGO_URI)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health')
def health():
    return {'status': 'ok'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))