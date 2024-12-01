from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Cafe {self.name}>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search_results', methods=['GET'])
def search_results():
    place = request.args.get('place')
    cafes = scrape_cafes(place)

    api_key = "YOUR_GOOGLE_MAPS_API_KEY"
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={api_key}"
    response = requests.get(geocode_url)
    location_data = response.json()

    latitude = 0.0
    longitude = 0.0
    if location_data['results']:
        latitude = location_data['results'][0]['geometry']['location']['lat']
        longitude = location_data['results'][0]['geometry']['location']['lng']

    return render_template('search_results.html', cafes=cafes, place=place, latitude=latitude, longitude=longitude)

@app.route('/cafe/<int:cafe_id>')
def cafe_detail(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    return render_template('cafe_detail.html', cafe=cafe)

def scrape_cafes(location):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(f"https://www.google.com/maps/search/cafes+in+{location}")
    time.sleep(5)

    cafes_data = []

    cafes = driver.find_elements(By.CLASS_NAME, 'section-result')
    for cafe in cafes:
        try:
            name = cafe.find_element(By.CLASS_NAME, 'section-result-title').text
            address = cafe.find_element(By.CLASS_NAME, 'section-result-location').text
            rating = float(cafe.find_element(By.CLASS_NAME, 'cards-rating-score').text)
            latitude, longitude = get_coordinates(cafe)

            cafe_entry = Cafe(
                name=name,
                address=address,
                rating=rating,
                description="N/A",
                latitude=latitude,
                longitude=longitude
            )
            db.session.add(cafe_entry)
            cafes_data.append(cafe_entry)
        except Exception as e:
            continue

    db.session.commit()
    driver.quit()

    return cafes_data

def get_coordinates(cafe):
    return (12.9716, 77.5946)

if __name__ == '__main__':
    app.run(debug=True)
