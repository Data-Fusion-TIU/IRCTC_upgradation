import pandas as pd
from app import app, db, Seat

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

if __name__ == "__main__":
    import_data()
