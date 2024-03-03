import sqlite3
import json
from datetime import datetime, timedelta
import random

# Establish connection to the SQLite database
connection = sqlite3.connect('database.db')

# Create the tables using the schema
with open('schema.sql') as f:
    connection.executescript(f.read())

# Initialize a cursor
cur = connection.cursor()

# Define the SQL statement to insert data into the flights table
sql = "INSERT INTO flights (origin_city, destination_city, airline, NoofConnection, depart_date, available_seates, price, Duration, Layover, BaggageInfo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

def get_dates():
    start_dt = datetime.now()
    end_dt = datetime(2024, start_dt.month, start_dt.day+2, start_dt.hour, 0)
    dt = start_dt + timedelta(seconds = random.randint(0, int((end_dt - start_dt).total_seconds())))
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

# Data to be inserted into the flights table
data = [
    ('NEW JERSEY', 'NEW YORK', 'INDIAN AIRWAYS', 0, datetime(2024,3,1,21), 100, 120,'2 Hrs', '0', '2-Piece 40 Kgs'),
    ('CALIFORNIA', 'NEW YORK', 'INDIAN AIRWAYS', 0, get_dates() , 100, 130,'2 Hrs', '0', '1-Piece 20 Kgs'),
    ('SEATTLE', 'NEW YORK', 'INDIAN AIRWAYS', 0, get_dates() , 100, 100,'2 Hrs', '0', '2-Piece 40 Kgs'),
    ('NEW JERSEY', 'LAS VEGAS', 'INDIAN AIRWAYS', 0, get_dates() , 100, 60,'2 Hrs', '0', '1-Piece 20 Kgs'),
    ('CALIFORNIA', 'LAS VEGAS', 'INDIAN AIRWAYS', 0, get_dates() , 100, 300,'2 Hrs', '0', '2-Piece 40 Kgs'),
    ('SEATTLE', 'LAS VEGAS', 'INDIAN AIRWAYS', 0, get_dates() , 100, 40,'2 Hrs', '0','1-Piece 20 Kgs'),
    ('NEW JERSEY', 'DALLAS', 'INDIAN AIRWAYS', 0, get_dates() , 100, 50,'2 Hrs', '0', '2-Piece 40 Kgs'),
    ('CALIFORNIA', 'DALLAS', 'INDIAN AIRWAYS', 0, get_dates() , 100, 300,'2 Hrs', '0','1-Piece 20 Kgs'),
    ('SEATTLE', 'DALLAS', 'INDIAN AIRWAYS', 0, get_dates() , 100, 30,'2 Hrs', '0','2-Piece 40 Kgs'),
    ('NEW JERSEY', 'NEW YORK', 'EMIRATES', 1, get_dates() , 100, 200,'4 Hrs', '2 Hrs','1-Piece 20 Kgs'),
    ('CALIFORNIA', 'NEW YORK', 'EMIRATES', 1, get_dates() , 100, 500,'5 Hrs', '2.5 Hrs','2-Piece 40 Kgs'),
    ('SEATTLE', 'NEW YORK', 'EMIRATES', 1, get_dates() , 100, 300,'4.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    ('NEW JERSEY', 'LAS VEGAS', 'EMIRATES', 1, get_dates() , 100, 70,'3 Hrs', '1.5 Hrs','2-Piece 40 Kgs'),
    ('CALIFORNIA', 'LAS VEGAS', 'EMIRATES', 1, get_dates() , 100, 400,'3 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    ('SEATTLE', 'LAS VEGAS', 'EMIRATES', 1, get_dates() , 100, 40,'2.5 Hrs', '0.5 Hrs','2-Piece 40 Kgs'),
    ('NEW JERSEY', 'DALLAS', 'EMIRATES', 1, get_dates() , 100, 50,'3.5 Hrs', '1.5 Hrs','1-Piece 20 Kgs'),
    ('CALIFORNIA', 'DALLAS', 'EMIRATES', 1, get_dates() , 100, 80,'4.5 Hrs', '2 Hrs','2-Piece 40 Kgs'),
    ('SEATTLE', 'DALLAS', 'EMIRATES', 1, get_dates() , 100, 100,'4.5 Hrs', '2 Hrs','1-Piece 20 Kgs'),
    ('NEW JERSEY', 'NEW YORK', 'DECCAN AIRWAYS', 0, get_dates() , 100, 60,'2 Hrs', '0','2-Piece 40 Kgs'),
    ('CALIFORNIA', 'NEW YORK', 'DECCAN AIRWAYS', 1, get_dates() , 100, 800,'3.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    ('SEATTLE', 'NEW YORK', 'DECCAN AIRWAYS', 0, get_dates() , 100, 30,'2 Hrs', '0','2-Piece 40 Kgs'),
    ('NEW JERSEY', 'LAS VEGAS', 'DECCAN AIRWAYS', 1, get_dates() , 100, 40,'2.5 Hrs', '1 Hrs','1-Piece 20 Kgs'),
    ('CALIFORNIA', 'LAS VEGAS', 'DECCAN AIRWAYS', 0, get_dates() , 100, 60,'2 Hrs', '0','1-Piece 20 Kgs'),
    ('SEATTLE', 'LAS VEGAS', 'DECCAN AIRWAYS', 1, get_dates() , 100, 50,'3 Hrs', '1.5 Hrs','2-Piece 40 Kgs'),
    ('NEW JERSEY', 'DALLAS', 'DECCAN AIRWAYS', 0, get_dates() , 100, 90,'2 Hrs', '0','1-Piece 20 Kgs'),
    ('CALIFORNIA', 'DALLAS', 'DECCAN AIRWAYS', 1, get_dates() , 100, 100,'3.5 Hrs', '0.5 Hrs','2-Piece 40 Kgs'),
    ('SEATTLE', 'DALLAS', 'DECCAN AIRWAYS', 0, get_dates() , 100, 500,'2 Hrs', '0','1-Piece 20 Kgs'),
]

# Insert data into the flights table
for i in data:
    cur.execute(sql, i)

connection.commit()

# Fetch all data from the flights table
cur.execute("SELECT * FROM flights")
flight_data = cur.fetchall()

# Close the database connection
connection.close()

## Convert fetched data to a list of dictionaries
flights_json = []
for flight in flight_data:
    flight_dict = {
        "origin_city": flight[0],
        "destination_city": flight[1],
        "airline": flight[2],
        "NoofConnection": flight[3],
        "depart_date": str(flight[4]),  # Convert datetime object to string
        "available_seates": flight[5],
        "price": flight[6],
        "Duration": flight[7],  # Include Duration in the JSON
        "Layover": flight[8],  # Include Layover in the JSON
        "BaggageInfo": flight[9] # Include BaggageInfo in the JSON
    }
    flights_json.append(flight_dict)

# Print the flight data in JSON format
print(json.dumps(flights_json, indent=4))

