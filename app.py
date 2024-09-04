from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///train_seats.db'
db = SQLAlchemy(app)

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


#@app.route('/confirmation', methods=['POST'])
#def confirmation():
    # Retrieve form data
#    full_name = request.form['full_name']
#    age = request.form['age']
#    gender = request.form['gender']
#    email = request.form['email']
#    phone = request.form['phone']
#    preferred_age_group = request.form['preferred_age_group']
    
    # Pass the form data to the confirmation page
#    return render_template('confirmation.html', name=full_name, phone=phone, age=age, gender=gender, age_group=preferred_age_group)

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
    
    # Pass the form data to the confirmation page
    return render_template('seat.html',  seats_dict=seats_dict, total_rows=total_rows, name=name, phone=phone, age=age, gender=gender, age_group=age_group)


@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)