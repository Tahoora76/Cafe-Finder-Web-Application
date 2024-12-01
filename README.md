# Cafe Finder Web Application

## Overview
The **Cafe Finder** web application allows users to search for cafes with Wi-Fi and remote working facilities based on their location. The application leverages web scraping using **Selenium** to gather cafe data from Google Maps and displays the results on a dynamic map. It provides an easy-to-use interface to find cafes based on user input and also offers detailed information about each cafe.

## Features
- User can input a location (city, area, etc.) to search for cafes.
- The application scrapes data from Google Maps to fetch cafe details.
- Displays search results on a map with café names, ratings, and addresses.
- Provides a detailed page for each cafe with more information.
- Uses **Flask** for backend functionality and **SQLAlchemy** to store scraped cafe data in a SQLite database.
- **Selenium** is used for web scraping Google Maps data.
- Interactive UI built using **HTML**, **CSS**, and **JavaScript**.

## Technologies Used
- **Flask**: Web framework for building the backend of the application.
- **SQLAlchemy**: ORM for managing the database and storing cafe data.
- **Selenium**: Web scraping tool for scraping cafe data from Google Maps.
- **Google Maps API**: Used for geocoding and retrieving coordinates of the searched location.
- **SQLite**: Lightweight database for storing cafe information.
- **HTML/CSS/JavaScript**: Frontend technologies for creating a responsive and user-friendly interface.
- **Jinja2**: Templating engine for rendering dynamic content on the web pages.

## Installation

### Prerequisites
- Python 3.x
- ChromeDriver (ensure it matches your Chrome version)
- Install the required Python packages:

```bash
pip install Flask Flask-SQLAlchemy selenium requests
```
Setting up the Database
To create the SQLite database and the cafes table, run the following commands in the Python shell:

``` bash
from app import db
db.create_all()
```
Google Maps API Key
You need a Google Maps API key to use the geocoding feature. To obtain an API key, follow the instructions from the Google Cloud Console. Add your API key in the code where indicated.

Running the Application
To run the Flask application, use the following command:

```bash
python app.py
```
Once the server is running, open your browser and go to http://127.0.0.1:5000/ to start using the Cafe Finder web app.
