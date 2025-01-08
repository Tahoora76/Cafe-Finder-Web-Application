from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import os
from Cafe_detail_Scrapper import Scrapper
import requests

# Selenium configuration
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-usb')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--v=1')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

# Global flag to track scraping status
scraping_in_progress = False
LAT_LON = None

def get_lat_long(city, api_key):
    # URL for OpenWeatherMap Geocoding API
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"

    # Make the GET request to the API
    response = requests.get(url)

    # Check if the response status is OK (200)
    if response.status_code == 200:
        data = response.json()

        # If data is available, extract latitude and longitude
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return [lat, lon]
        else:
            return None, None  # No data found
    else:
        print("Error fetching data from OpenWeatherMap API")
        return None, None  # API request failed






# Flask app setup
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    location = request.form.get('location')
    lat_lon = get_lat_long(location, "4ee8489b3062de9b6fd9731f101fbbea")
    LAT_LON = lat_lon

    if location:
        def run_scraper():
            Scrapper(location)  # Run the main scraper
            return redirect(url_for('result'))

        # Start the scraper in a separate thread
        thread = threading.Thread(target=run_scraper)
        thread.start()

        # Redirect to loading page
        return redirect(url_for('loading'))
    else:
        return "Location is required", 400


@app.route('/loading')
def loading():
    return render_template('loading.html')


@app.route('/results', methods=['GET'])
def results():
    if scraping_in_progress:
        return jsonify({"message": "Data is still being scraped. Please check back later."}), 202

    try:
        with open('cafe_details.json', 'r') as file:
            cafes = json.load(file)
        return render_template('result.html', cafes=cafes)
    except FileNotFoundError:
        return jsonify({"message": "No data found. Please start a search first."}), 404


@app.route('/cafe_detail')
def cafe_detail():
    cafe_name = request.args.get('name')  # Get the name parameter from the URL

    # Load the cafe details from the JSON file
    with open('cafe_details.json', 'r') as file:
        cafes_data = json.load(file)

    # Find the cafe by its name
    cafe = next((c for c in cafes_data if c["Name"] == cafe_name), None)

    if cafe:
        return render_template('cafe_detail.html', cafe=cafe)
    else:
        return "Cafe not found", 404


if __name__ == '__main__':
    app.run(debug=True)
