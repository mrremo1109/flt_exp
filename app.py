from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import sqlite3
from datetime import datetime
import os
print(os.getcwd())
import googlemaps
import requests

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(sql, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    if sql.strip().lower().startswith('select'):
        res = cursor.fetchall()
    else:
        conn.commit()
        res = None
    cursor.close()
    conn.close()
    return res

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/currency_rates')
def currency_rates():
    # Define your currency rates
    rates = {
        "USD": 1.0,
        "EUR": 0.85,
        "GBP": 0.73,
        "JPY": 150.09,
        "IQD": 0.31,
        "INR": 82.85,
    }
    
    # Return the currency rates as JSON response
    return jsonify(rates)

def get_all_flights():
    conn = sqlite3.connect('flights.db')  # Replace 'your_database.db' with your SQLite database file path
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    conn.close()
    return flights

@app.route('/api/flights_data')
def get_flights_data():
    flights = get_all_flights()
    # Convert fetched flight data to a list of dictionaries
    flights_data = [{'origin_city': row[0], 'destination_city': row[1], 'depart_date': row[2], 'airline': row[3], 'NoofConnection': row[4], 'Duration': row[5], 'Layover': row[6], 'price': row[7]} for row in flights]
    return jsonify({'flights': flights_data})


""""
@app.route('/api/flights_data', methods=['GET', 'POST'])
def get_flights_data():
    # 1. Fetch data from the database
    sql = "SELECT * FROM flights"  # Modify the query as needed
    flights_data = execute_query(sql)

    # 2. Check if data is retrieved successfully
    if not flights_data:
        return jsonify({"error": "No flights data found"}), 404  # Return error for not found

    # 3. Convert data to list of dictionaries (suitable for JSON)
    flights_list = []
    for row in flights_data:
        flight_dict = {
            "origin_city": row[0],
            "destination_city": row[1],
            "airline": row[2],
            "NoofConnection": row[3],
            "depart_date": str(row[4]), 
            "available_seates": row[5],
            "price": row[6],
            "Duration": row[7],  # Include Duration in the JSON
            "Layover": row[8],  # Include Layover in the JSON
            "BaggageInfo": row[9]   # Include Baggage Info in the
            # ... add other relevant columns and their corresponding values
        }
        flights_list.append(flight_dict)

    # 4. Return data as JSON
    return jsonify(flights_list)"""

@app.route('/api/airline', methods=['GET', 'POST'])
def get_airline():
    # 1. Fetch data from the database
    sql = "SELECT DISTINCT airline FROM flights"  # Modify the query to select unique airline values
    airline_data = execute_query(sql)

    # 2. Check if data is retrieved successfully
    if not airline_data:
        return jsonify({"error": "No flights data found"}), 404  # Return error for not found

    # 3. Extract airline details from the fetched data
    airline_details = [row[0] for row in airline_data]  # Assuming airline is the first column

    # 4. Remove duplicates
    unique_airline_details = list(set(airline_details))

    # 5. Return airline details as JSON
    return jsonify(unique_airline_details)

@app.route('/api/origincity', methods=['GET', 'POST'])
def get_Origincity():
    # 1. Fetch data from the database
    sql = "SELECT DISTINCT origin_city FROM flights"  # Modify the query to select unique airline values
    origin_data = execute_query(sql)

    # 2. Check if data is retrieved successfully
    if not origin_data:
        return jsonify({"error": "No flights data found"}), 404  # Return error for not found

    # 3. Extract airline details from the fetched data
    origin_details = [row[0] for row in origin_data]  # Assuming airline is the first column

    # 4. Remove duplicates
    unique_origin_details = list(set(origin_details))

    # 5. Return airline details as JSON
    return jsonify(unique_origin_details)

@app.route('/api/destinationcity', methods=['GET', 'POST'])
def get_destinationcity():
    # 1. Fetch data from the database
    sql = "SELECT DISTINCT destination_city FROM flights"  # Modify the query to select unique airline values
    destination_data = execute_query(sql)

    # 2. Check if data is retrieved successfully
    if not destination_data:
        return jsonify({"error": "No flights data found"}), 404  # Return error for not found

    # 3. Extract airline details from the fetched data
    destination_details = [row[0] for row in destination_data]  # Assuming airline is the first column

    # 4. Remove duplicates
    unique_destination_details = list(set(destination_details))

    # 5. Return airline details as JSON
    return jsonify(unique_destination_details)

@app.route('/api/departuredate', methods=['GET', 'POST'])
def get_departuredate():
    # 1. Fetch data from the database
    sql = "SELECT DISTINCT depart_date FROM flights"  # Modify the query to select unique airline values
    departuredate_data = execute_query(sql)

    # 2. Check if data is retrieved successfully
    if not departuredate_data:
        return jsonify({"error": "No flights data found"}), 404  # Return error for not found

    # 3. Extract airline details from the fetched data
    departuredate_details = [row[0] for row in departuredate_data]  # Assuming airline is the first column

    # 4. Remove duplicates
    unique_departuredate_details = list(set(departuredate_details))

    # 5. Return airline details as JSON
    return jsonify(unique_departuredate_details)

@app.route('/api/Duration', methods=['GET', 'POST'])
def get_Duration():
    # 1. Fetch data from the database
    sql = "SELECT Duration FROM flights"  # Modify the query as needed
    Duration_data = execute_query(sql)

    # 2. Check if data is retrieved successfully
    if not Duration_data:
        return jsonify({"error": "No flights data found"}), 404  # Return error for not found

    # 3. Extract and format data for JSON serialization
    durations = []
    for row in Duration_data:
        # Replace 'Duration' with the correct column name from your database
        durations.append({"Duration": row['Duration']})  # Adapt based on actual column names

    # 4. Return the serialized data
    return jsonify(durations)


@app.route('/api/search', methods=['GET'])
def search_data():
    origin_city = request.args.get('originCity')
    destination_city = request.args.get('destinationCity')
    airline = request.args.get('airline')  # Get the airline parameter from the query string
    
    # Modify SQL query to filter by airline as well
    if airline:  # Only add airline to the filter if it's provided
        sql = "SELECT * FROM flights WHERE origin_city=? AND destination_city=? AND airline=?"
        query_parameters = (origin_city, destination_city, airline)
    else:
        sql = "SELECT * FROM flights WHERE origin_city=? AND destination_city=?"
        query_parameters = (origin_city, destination_city)
    
    # Execute the query with the additional airline parameter if it's been provided
    flights = execute_query(sql, query_parameters)
    
    # Log the number of flights found
    app.logger.info(f"Number of flights found: {len(flights)}")
    
    # Check if flights are found
    if not flights:
        return jsonify({"error": "No flights found for the provided criteria"}), 404
    
    # Serialize flight details into JSON format
    serialized_flights = []
    for flight in flights:
        serialized_flight = {
            "origin_city": flight["origin_city"],
            "destination_city": flight["destination_city"],
            "depart_date": flight["depart_date"],
            "airline": flight["airline"],
            "NoofConnection": flight["NoofConnection"],
            "Duration": flight["Duration"],
            "Layover": flight["Layover"],
            "price": flight["price"]
        }
        serialized_flights.append(serialized_flight)
    
    # Return flight details in JSON format
    return jsonify(serialized_flights)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/bookingdetails', methods=['POST'])
def bookingdetails():
    flight_details = request.form.to_dict()
    return render_template('bookingdetails.html', flight_details=flight_details)


GOOGLE_MAPS_API_KEY = 'AIzaSyCHfcbLvLze_Uz57qc1Wl4H1TWQ2E_dv5E'
OPENWEATHER_API_KEY = '9cc7cb0d46d0878a0faa22cecf727c72' 


def get_nearby_attractions(dest_coord, api_key):
    # Google Places API - Nearby Search request
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': dest_coord,
        'radius': '5000',  # Search within a 5 km radius
        'type': 'tourist_attraction',
        'key': api_key
    }
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
        attractions = response.json()['results']
    else:
        attractions = []
    return attractions

def get_weather_info(city_name, openweather_api_key):
    # OpenWeatherMap API request
    endpoint_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': openweather_api_key,
        'units': 'metric'
    }
    response = requests.get(endpoint_url, params=params)
    if response.status_code == 200:
        weather_info = response.json()
    else:
        weather_info = {}
    return weather_info

@app.route('/finalize_booking', methods=['POST'])
def finalize_booking():
    print("Form Data:", request.form)

    # Part 1: Update flight availability
    flight_details = request.form.to_dict()
    sql = "UPDATE flights SET available_seates=available_seates-1 WHERE origin_city=? AND destination_city=? AND airline=?"
    params = (flight_details['origin_city'], flight_details['destination_city'], flight_details['airline'])
    execute_query(sql, params) 
    # Assuming execute_query is a function that executes the SQL command
    
    # Part 2: Generate directions and map
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    directions = gmaps.directions(flight_details['origin_city'], flight_details['destination_city'], mode="driving")

    distance = directions[0]['legs'][0]['distance']['text']
    route_steps = [step['html_instructions'] for step in directions[0]['legs'][0]['steps']]
    polyline = directions[0]['overview_polyline']['points']
    origin_coord = f"{directions[0]['legs'][0]['start_location']['lat']},{directions[0]['legs'][0]['start_location']['lng']}"
    dest_coord = f"{directions[0]['legs'][0]['end_location']['lat']},{directions[0]['legs'][0]['end_location']['lng']}"
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=550x620&path=enc:{polyline}&key={GOOGLE_MAPS_API_KEY}"
    all_attractions = get_nearby_attractions(dest_coord, GOOGLE_MAPS_API_KEY)
    limited_attractions = all_attractions[:10]
    weather_info = get_weather_info(flight_details['destination_city'], OPENWEATHER_API_KEY)

    # Render template with all the information
    return render_template(
        'finalize_booking.html',
        flight_details=flight_details,
        distance=distance,
        route_steps=route_steps,
        map_url=map_url,
        attractions=limited_attractions,
        weather=weather_info,
    )