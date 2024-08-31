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


@app.route('/confirmation', methods=['POST'])
def confirmation():
    # Retrieve form data
    name = request.form['name']
    phone = request.form['phone']
    age = request.form['age']
    gender = request.form['gender']
    age_group = request.form['age_group']
    
    # Pass the form data to the confirmation page
    return render_template('confirmation.html', name=name, phone=phone, age=age, gender=gender, age_group=age_group)

@app.route('/seat')
def seat():
    # available_seats = Seat.query.filter_by(is_booked=False).all()
    # seats = Seat.query.all()  # Fetch all seats
    return render_template('seat.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)