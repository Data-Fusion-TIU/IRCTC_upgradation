from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')
    #return 'Hello, World!'

@app.route('/trains')
def train_selection():
    return render_template('trains.html')

@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/book')
def book_form():
    return render_template('book.html')


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

@app.route('/seating')
def seating():
    return render_template('seating.html')
if __name__ == "__main__":
    app.run(debug=True)