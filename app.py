from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests
from Seat_booking import TrainBookingSystem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///train_seats.db'
db = SQLAlchemy(app)

RAPIDAPI_KEY = '3e7fabd9demsh258d5b8afd8208bp13c862jsna4d0ee130389'


# Define the Seat model
class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_age = db.Column(db.Integer, nullable=False)
    preferred_age_group = db.Column(db.String(20), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    seat_type = db.Column(db.String(20), nullable=False)
    is_booked = db.Column(db.Boolean, default=False)  # New attribute to track booking status


@app.route('/')
def home():
    return render_template('index.html')
    #return 'Hello, World!'

@app.route('/passenger')
def passenger():
    return render_template('passenger.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/get_trains', methods=['POST'])
def get_trains():
    data = request.json
    from_station = data.get('from')
    to_station = data.get('to')
    journey_date = data.get('journeyDate')


    if not from_station or not to_station or not journey_date:
        return jsonify({'error': 'Missing from station, to station, or journey date'}), 400

    headers = {
        'x-rapidapi-host': 'irctc1.p.rapidapi.com',
        'x-rapidapi-key': '3e7fabd9demsh258d5b8afd8208bp13c862jsna4d0ee130389'
    }
    
    url = f'https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations?fromStationCode={from_station}&toStationCode={to_station}&dateOfJourney={journey_date}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Log the raw response
        train_data = response.json()
        print('API Response:', train_data)  # Debugging purpose
        
        if 'status' in train_data and train_data['status'] == True and 'data' in train_data:
            return jsonify(train_data)
        else:
            return jsonify({'error': 'Unexpected data format or no data available'}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/seat', methods=['POST'])
def seat():
    seats = Seat.query.all()
    seats_dict = {seat.seat_number: (seat.user_age is not None) for seat in seats}

    total_seats = len(seats_dict)
    seats_per_row = 6  # 3 + 1 + 2 configuration
    total_rows = (total_seats + seats_per_row - 1) // seats_per_row
    name = request.form['full name']
    phone = request.form['phone']
    age = request.form['age']
    gender = request.form['gender']
    age_group = request.form['age_group']
    booking_data = pd.read_csv('train_booking_data.csv')
    booking_system = TrainBookingSystem(booking_data)
    recommended_seats = booking_system.get_recommended_seats(age_group)

    
    # Pass the form data to the confirmation page
    return render_template('seat.html',  seats_dict=seats_dict, total_rows=total_rows, name=name, phone=phone, age=age, gender=gender, age_group=age_group, recommendation=recommended_seats)

@app.route('/pay_and_confirm')
def confirmed():
    return render_template('pay_and_confirm.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)