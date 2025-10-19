import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
import requests
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
NASA_API_KEY = os.getenv("NASA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database()  # 
users = db.users


# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.find_one({"username": username, "password": password})
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if users.find_one({"username": username}):
            return render_template('register.html', error="Username already exists")
        users.insert_one({"username": username, "password": password, "email": email})
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch last 6 APOD images
    end_date = datetime.today()
    start_date = end_date - timedelta(days=5)
    apod_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&start_date={start_date.date()}&end_date={end_date.date()}"
    try:
        response = requests.get(apod_url)
        data = response.json()
    except:
        data = []

    return render_template('dashboard.html', data=data, username=session['username'])

@app.route('/get_insight', methods=['POST'])
def get_insight():
    img_data = request.json
    prompt = f"Describe this Astronomy Picture of the Day in an interesting cosmic way:\nTitle: {img_data['title']}\nDate: {img_data['date']}\nDescription: {img_data['explanation']}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role":"system", "content":"You are a helpful astronomy assistant."},
                {"role":"user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.8
        )
        insight = response['choices'][0]['message']['content']
    except Exception as e:
        insight = "Could not fetch insight at the moment."
    
    return jsonify({"insight": insight})

if __name__ == '__main__':
    app.run(debug=True)
