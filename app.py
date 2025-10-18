from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from pymongo import MongoClient
import os, bcrypt, requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Config
app.secret_key = os.getenv("SECRET_KEY", "defaultsecret")
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client['cosmicscope']
users_collection = db['users']


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').encode('utf-8')

        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return render_template('register.html', error="Username already exists!")

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        users_collection.insert_one({'username': username, 'email': email, 'password': hashed})

        session['user'] = username
        return redirect(url_for('dashboard'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').encode('utf-8')

        user = users_collection.find_one({'username': username})
        if user and bcrypt.checkpw(password, user['password']):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Fetch NASA APOD data
    apod_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    data = requests.get(apod_url).json()

    return render_template('dashboard.html', apod=data, user=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
