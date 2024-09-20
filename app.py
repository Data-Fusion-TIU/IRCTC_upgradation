from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests
from Seat_booking import TrainBookingSystem
from Train_Booking import TrainReservationSystem 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///train_seats.db'
db = SQLAlchemy(app)

def import_data():
    with app.app_context():
        # Load the Excel file
        excel_file = 'train_booking_data.csv'  # Update this with the path to your Excel file
        df = pd.read_csv(excel_file)
        # Clear existing seat data
        Seat.query.delete()
        db.session.commit()
        
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
        'x-rapidapi-key': 'f9face5ff2mshd18a614949f1911p185075jsnc7b7dfeff4dc'
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
    # Retrieve all seat data
    seats = Seat.query.all()
    print("Retrieved Seats:", seats)
    seats_dict = {seat.seat_number: (seat.user_age is not None) for seat in seats}

    print("Seats Dictionary:", seats_dict)

    # Calculate total seats and rows
    total_seats = len(seats_dict)
    seats_per_row = 6  # 3 + 1 + 2 configuration
    total_rows = (total_seats + seats_per_row - 1) // seats_per_row

    # Extract passenger details from the form data
    passengers = []
    i = 1
    while True:
        full_name = request.form.get(f'passenger{i}_full_name')
        if full_name is None:
            break  # Exit loop if no more passenger data
        
        # Collect all details for the passenger
        passenger = {
            'full_name': full_name,
            'age': request.form.get(f'passenger{i}_age'),
            'phone': request.form.get(f'passenger{i}_phone'),
            'gender': request.form.get(f'passenger{i}_gender'),
            'age_group': request.form.get(f'passenger{i}_age_group'),
        }
        passengers.append(passenger)
        i += 1

    # Count the number of passengers
    num_passengers = len(passengers)
    
    # Load booking data and initialize the booking system
    booking_data = pd.read_csv('train_booking_data.csv')
    booking_system = TrainBookingSystem(booking_data)

    # Check available seats manually by iterating from 1 to 108
    available_seats = []
    for seat_number in range(1, 109):  # Assuming seat numbers range from 1 to 108
        if seat_number not in seats_dict or not seats_dict[seat_number]:
            available_seats.append(seat_number)

    # Print available seats for debugging
    print(f"Available seats: {available_seats}")

    def find_nearby_seats(num_seats, available_seats):
        # Helper function to find contiguous blocks of seats
        for i in range(len(available_seats) - num_seats + 1):
            if all(seat not in seats_dict or not seats_dict[seat] for seat in available_seats[i:i + num_seats]):
                return available_seats[i:i + num_seats]
        return None

    def recommend_seats(num_seats, available_seats):
        # Main function to recommend seats
        nearby_seats = find_nearby_seats(num_seats, available_seats)
        if nearby_seats:
            return nearby_seats
        
        # Alternative recommendations: Provide best options if contiguous seats are not available
        best_options = []
        for seat_number in available_seats:
            if len(best_options) < num_seats:
                best_options.append(seat_number)
            else:
                break
        return best_options if len(best_options) == num_seats else None

    if num_passengers == 1:
        if available_seats:
            # Handle single passenger case
            passenger = passengers[0]
            recommended_seats = booking_system.get_recommended_seats(passenger['age_group'])
            print("Passenger details:", passenger)
            print("Recommended seats:", recommended_seats)
            
            return render_template('seat.html', 
                                   seats_dict=seats_dict, 
                                   total_rows=total_rows, 
                                   passengers=passengers, 
                                   recommendation=recommended_seats)
        else:
            # No seats available
            return render_template('seat.html', 
                                   seats_dict=seats_dict, 
                                   total_rows=total_rows, 
                                   passengers=None, 
                                   recommendation=None,
                                   message="No seats available.")
    
    else:
        if len(available_seats) >= num_passengers:
            # Handle multiple passengers case
            #recommended_seats = recommend_seats(num_passengers, available_seats)
            recommended_seats = []
            if recommended_seats:
                # Use the recommended seats if available
                print("Passengers details:", passengers)
                print("Recommended seats:", recommended_seats)
                
                return render_template('seat.html', 
                                       seats_dict=seats_dict, 
                                       total_rows=total_rows, 
                                       passengers=passengers, 
                                       recommendation=recommended_seats)
            else:
                # Fallback if no suitable recommendations are found
                fallback_seats = []
                print("Fallback seats:", fallback_seats)
                
                return render_template('seat.html', 
                                       seats_dict=seats_dict, 
                                       total_rows=total_rows, 
                                       passengers=passengers, 
                                       recommendation=fallback_seats)
        else:
            # Not enough seats available
            return render_template('seat.html', 
                                   seats_dict=seats_dict, 
                                   total_rows=total_rows, 
                                   passengers=None, 
                                   recommendation=None,
                                   message="Not enough seats available.")

@app.route('/pay_and_confirm')
def confirm_booking():
   return render_template('payment.html')

@app.route('/update_dataset', methods=['POST'])
def update_dataset():
    try:
        # Retrieve data from the JSON payload
        data = request.get_json()
        seat_numbers = data.get('seatNumber')  # Get the list of seat numbers
        passengers = data.get('passengers')     # Get the array of passengers
        seat_numbers = [int(seat.strip()) for seat in seat_numbers.split(',') if seat.strip()]

        # Define CSV file path
        csv_file_path = 'train_booking_data.csv'
        print("csv file okay")
        # Read the current dataset
        df = pd.read_csv(csv_file_path)

        # Ensure the number of passengers matches the number of seats
        if len(seat_numbers) != len(passengers):
            return "The number of passengers and seats do not match", 400

        # Loop through each passenger and their corresponding seat
        for passenger, seat_number in zip(passengers, seat_numbers):
            user_age = passenger.get('age')
            print(user_age)
            preferred_age_group = passenger.get('age_group')
            print(preferred_age_group)

            # Generate the next Booking ID
            booking_id = df['Booking ID'].max() + 1 if not df.empty else 1

            # Extract row and column information based on the seat number
            row = ((int(seat_number) - 1) // 6) + 1
            column = ((int(seat_number) - 1) % 6) + 1

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
                'Seat Type': [seat_type],
                'Seat Booked': [True]
            })

            # Append new row to the DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

        # Save updated DataFrame back to CSV
        df.to_csv(csv_file_path, index=False)

        return redirect(url_for('success'))  # Redirect to a success page or home page

    except Exception as e:
        # Handle any errors that occur during processing
        print(f"An error occurred: {e}")
        return redirect(url_for('signin'))  # Redirect to an error page or handle accordingly

@app.route('/success')
def success():
    return render_template('pay_and_confirm.html')

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

@app.route('/signin')
def signin():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)