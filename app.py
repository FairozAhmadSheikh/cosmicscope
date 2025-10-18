from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get secret key and NASA API key from .env file
app.secret_key = os.getenv("SECRET_KEY", "defaultsecret")
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

# Dummy user database (you can later replace it with MongoDB)
users = {}


#   ROUTES  =

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple authentication
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users:
            return render_template('register.html', error="Username already exists.")
        else:
            users[username] = password
            session['user'] = username
            return redirect(url_for('dashboard'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Fetch NASA Astronomy Picture of the Day
    apod_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    data = requests.get(apod_url).json()

    return render_template("dashboard.html", apod=data, user=session['user'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


#   MAIN  

if __name__ == '__main__':
    app.run(debug=True)
