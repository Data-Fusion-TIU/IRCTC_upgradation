import pandas as pd
from sklearn.cluster import KMeans

class TrainBookingSystem:
    def __init__(self, booked_seats_data):
        self.total_rows = 17
        self.total_cols = 6
        self.seats = [['O' for _ in range(1, self.total_cols + 1)] for _ in range(1, self.total_rows + 1)]
        self.booked_seats = {}
        self.base_seat_price = 800  
        booked_seats_data['Age Group Encoded'] = pd.Categorical(booked_seats_data['Preferred Age Group']).codes

        for index, row in booked_seats_data.iterrows():
            if row['Seat Booked'] == 1:
                seat_number = row['Seat Number']
                age_group = row['Preferred Age Group']
                self.booked_seats[seat_number] = age_group
                self.seats[row['Row'] - 1][row['Column'] - 1] = 'X'

        self.cluster_model = self.train_clustering_model(booked_seats_data)

    def train_clustering_model(self, booked_seats_data):
        X = booked_seats_data[['Row', 'Column', 'Age Group Encoded']]
        kmeans = KMeans(n_clusters=5, random_state=42)
        booked_seats_data['Cluster'] = kmeans.fit_predict(X)
        self.booked_seats_data = booked_seats_data
        return kmeans

    def get_recommended_seats(self, age_group):
        recommended = []

        age_groups = ['18-25', '25-40', '40-60', '60+']
        age_group_label = pd.Categorical([age_group], categories=age_groups).codes[0]

        features_list = []
        for r in range(1, self.total_rows + 1):
            for c in range(1, self.total_cols + 1):
                seat_number = (r - 1) * self.total_cols + c
                if seat_number not in self.booked_seats:
                    if self.is_adjacent_seat_available(r, c, age_group):
                        features_list.append({
                            'Row': r,
                            'Column': c,
                            'Age Group Encoded': age_group_label
                        })

        features = pd.DataFrame(features_list)
        if not features.empty:
            clusters = self.cluster_model.predict(features)
            for i, row in features.iterrows():
                seat_number = (row['Row'] - 1) * self.total_cols + row['Column']
                cluster_label = clusters[i]
                if self.is_adjacent_seat_in_cluster(row['Row'], row['Column'], cluster_label, age_group):
                    recommended.append(seat_number)

        return recommended
    
    def is_adjacent_seat_available(self, row, col, age_group):
        adjacent_seats = [
            (row, col - 1), (row, col + 1)
        ]
        for r, c in adjacent_seats:
            if 1 <= r <= self.total_rows and 1 <= c <= self.total_cols:
                seat_number = (r - 1) * self.total_cols + c
                if seat_number in self.booked_seats and self.booked_seats[seat_number] == age_group:
                    return True
        return False

    def is_adjacent_seat_in_cluster(self, row, col, cluster_label, age_group):
        adjacent_seats = [
            (row, col - 1), (row, col + 1)
        ]
        for r, c in adjacent_seats:
            if 1 <= r <= self.total_rows and 1 <= c <= self.total_cols:
                seat_number = (r - 1) * self.total_cols + c
                features = pd.DataFrame([{
                    'Row': r,
                    'Column': c,
                    'Age Group Encoded': pd.Categorical([age_group], categories=['18-25', '25-40', '40-60', '60+']).codes[0]
                }])
                cluster = self.cluster_model.predict(features)[0]
                if cluster == cluster_label:
                    return True
        return False


    def book_seat(self, seat_number, age_group):
        row = (seat_number - 1) // self.total_cols + 1
        col = (seat_number - 1) % self.total_cols + 1

        self.booked_seats[seat_number] = age_group
        self.seats[row - 1][col - 1] = 'X'

