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

    username = session['username']
    nasa_api_key = os.getenv("NASA_API_KEY")

    today = datetime.utcnow().date()
    start_date = today - timedelta(days=3)

    nasa_url = (
        f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}"
        f"&start_date={start_date}&end_date={today}"
    )

    try:
        response = requests.get(nasa_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Ensure it's a list
        if isinstance(data, dict):
            data = [data]

    except Exception as e:
        print(f"⚠️ NASA API error: {e}")
        # Fallback demo data if NASA API fails
        data = [
            {
                "title": "Cosmic Nebula Simulation",
                "url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745",
                "date": str(today),
                "explanation": "Fallback image — showing due to NASA API timeout.",
            },
            {
                "title": "Galactic Horizon",
                "url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d",
                "date": str(today - timedelta(days=1)),
                "explanation": "A breathtaking view of the Milky Way captured in long exposure.",
            },
        ]

    return render_template("dashboard.html", username=username, data=data)

@app.route("/insight", methods=["GET"])
def insight():
    try:
        nasa_api_key = os.getenv("NASA_API_KEY")
        mars_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos?api_key={nasa_api_key}"
        response = requests.get(mars_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            photos = data.get("latest_photos", [])
            if photos:
                photo = photos[0]
                return jsonify({
                    "photo_url": photo["img_src"],
                    "camera": photo["camera"]["full_name"],
                    "rover": photo["rover"]["name"],
                    "earth_date": photo["earth_date"]
                })
            else:
                return jsonify({"error": "No recent rover data found."}), 404
        else:
            return jsonify({"error": "Failed to reach NASA servers."}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/get_insight', methods=['POST'])
def get_insight():
    img_data = request.get_json()  # safer than request.json
    prompt = (
        f"Describe this Astronomy Picture of the Day in an interesting cosmic way:\n"
        f"Title: {img_data.get('title')}\n"
        f"Date: {img_data.get('date')}\n"
        f"Description: {img_data.get('explanation')}"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful astronomy assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.8
        )
        # extract the assistant's message
        insight = response.choices[0].message.content
    except Exception as e:
        print("OpenAI API error:", e)  # logs the real error in terminal
        insight = "Could not fetch insight at the moment."

    return jsonify({"insight": insight})

@app.route('/explore')
def explore():
    api_key = os.getenv("NASA_API_KEY")
    mars_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={api_key}"
    try:
        response = requests.get(mars_url, timeout=10)
        data = response.json().get('photos', [])[:12]
    except Exception as e:
        print("Error fetching Mars data:", e)
        data = []
    return render_template('explore.html', photos=data)


if __name__ == '__main__':
    app.run(debug=True)
