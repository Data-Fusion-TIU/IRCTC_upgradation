from flask import Flask, render_template, request
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

@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        age = request.form.get('age')
        gender = request.form.get('gender')
        age_group = request.form.get('age_group')
        
        # Process the data or save it as needed
        # For example, you can print it to the console
        print(f"Name: {name}")
        print(f"Phone Number: {phone}")
        print(f"Age: {age}")
        print(f"Gender: {gender}")
        print(f"Preferred Age Group: {age_group}")
        return render_template('book.html', name=name)

    return render_template('details.html')

@app.route('/book')
def seat_arrangement():
    return render_template('book.html')
if __name__ == "__main__":
    app.run(debug=True)