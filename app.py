from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests
from Seat_booking import TrainBookingSystem
from Train_Booking import TrainReservationSystem 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///train_seats.db'
db = SQLAlchemy(app)


# Load the Excel file
excel_file = 'train_booking_data.csv'  # Update this with the path to your Excel file
df = pd.read_csv(excel_file)

# Ensure your Excel columns match the expected names
# You might need to adjust column names based on your Excel file
def import_data():
    with app.app_context():
        # Clear existing data (optional)
        db.drop_all()
        db.create_all()

        # Iterate through the DataFrame and add rows to the database
        for _, row in df.iterrows():
            seat = Seat(
                user_age=row['User Age'],
                preferred_age_group=row['Preferred Age Group'],
                seat_number=row['Seat Number'],
                row=row['Row'],         # Make sure your Excel file has a 'Row' column
                column=row['Column'],   # Make sure your Excel file has a 'Column' column
                seat_type=row['Seat Type'],
                is_booked=row['Seat Booked'] 
            )
            db.session.add(seat)
        
        db.session.commit()
        print("Data imported successfully.")


@app.route('/import_csv')
def import_csv():
    # Load the CSV
    booking_data = pd.read_csv('train_booking_data.csv')
    
    # Clear existing seat data
    Seat.query.delete()
    db.session.commit()

    # Insert new data
    for _, row in booking_data.iterrows():
        seat = Seat(
            user_age=row['User Age'],
            preferred_age_group=row['Preferred Age Group'],
            seat_number=row['Seat Number'],
            row=row['Row'],
            column=row['Column'],
            seat_type=row['Seat Type'],
            is_booked=row['Seat Booked'] == 'TRUE'
        )
        db.session.add(seat)
    db.session.commit()

    return 'CSV Data Imported Successfully'


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
    import_data()
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
        'x-rapidapi-key': 'ee040acf61msh53566421b683633p102e29jsnd186e4fc7f7d'
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
    name = request.form['full_name']
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
def confirm_booking():
   return render_template('payment.html')



@app.route('/update_dataset', methods=['POST'])
def update_dataset():
    # Retrieve data from the form
    seat_number = int(request.form['seat_number'])
    user_age = request.form['user_age']
    preferred_age_group = request.form['preferred_age_group']
    # seat_booked = request.form['seat_booked']

    # Define CSV file path
    csv_file_path = 'train_booking_data.csv'

    # Load existing dataset
    df = pd.read_csv(csv_file_path)

    # Generate the next Booking ID
    booking_id = df['Booking ID'].max() + 1 if not df.empty else 1

    # Extract row and column information (you may need additional logic for this)
    # For demonstration, assuming row and column are derived from seat number
    row = ((seat_number - 1) // 6) + 1
  # Example logic, adjust as necessary
    column = ((seat_number - 1) % 6)+1  # Example logic, adjust as necessary
            # Determine seat type based on the column
    if column == 1 or column == 6:
        seat_type = "Window"
    elif column == 2 or column == 5:
        seat_type = "Middle"
    else:
        seat_type = "Aisle"

# Create a new row for the dataset as a DataFrame
    new_row = pd.DataFrame({
        'Booking ID': [booking_id],
        'User Age': [user_age],
        'Preferred Age Group': [preferred_age_group],
        'Seat Number': [seat_number],
        'Row': [row],
        'Column': [column],
        'Seat Type': [seat_type],  # Adjust as needed
        'Seat Booked': True
    })


    # Append new row to the DataFrame
    df = pd.concat([df, new_row], ignore_index=True)

    # Save updated DataFrame back to CSV
    df.to_csv(csv_file_path, index=False)

    return redirect(url_for('success'))  # Redirect to a success page or home page

@app.route('/success')
def success():
    return render_template('pay_and_confirm.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

system = TrainReservationSystem('Gitanjali Express Route.csv')
@app.route('/get_nearby_stations', methods=['POST'])
def get_nearby_stations_route():
    try:
        data = request.get_json()  # Get the JSON data sent from the frontend
        from_station = data.get('fromStation')
        to_station = data.get('toStation')

        # Fetch nearby stations (this can be from a database or external API)
        available_stations = system.find_best_station(from_station, to_station)
        # nearby_stations = [('RIG', 4, 175), ('CKP', 12, 101), ('TATA', 16, 163)]
        print("From: ", from_station)
        print("To: ", to_station)
        print("Nearby Stations:", available_stations)  # Debugging purpose
        return jsonify({
            "nearbyStations": available_stations,
            "status": True
        }), 200

    except Exception as e:
        print(f"Error Occured: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": False
        }), 500


if __name__ == "__main__":
    app.run(debug=True)