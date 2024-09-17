import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import datetime

class TrainReservationSystem:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df_cleaned = None
        self.dynamic_distance = None
        self.model = None
        self.setup_system()

    def setup_system(self):
        self.df_cleaned = self.load_and_clean_data()
        self.dynamic_distance = self.get_dynamic_distance()
        self.label_days()  # Add day labeling for stations
        self.train_model()

    def load_and_clean_data(self):
        # Load the data from CSV, assuming the file has the necessary columns
        data = pd.read_csv(self.data_file)
        # Retain the necessary columns
        df_cleaned = data.drop(columns=['Stop Time(MIN)'])
        return df_cleaned

    def get_dynamic_distance(self):
        today = datetime.datetime.now()
        is_holiday = today.weekday() in [5, 6]  # Weekends as holidays
        return 200 if is_holiday else 250

    def label_days(self):
        """ Label each station as either Day 1 or Day 2 based on the station departure time """
        day = 1
        self.df_cleaned['Day'] = 1  # Start by assuming everything is Day 1
        rig_idx = self.df_cleaned[self.df_cleaned['Station Name'] == 'RIG'].index[0]  # Find index of RIG station

        # From BSP onwards, mark all stations as Day 2
        for idx in range(rig_idx + 1, len(self.df_cleaned)):
            self.df_cleaned.at[idx, 'Day'] = 2

    def label_stations_within_distance(self, index, distance):
        total_distance = 0
        for idx in range(index, len(self.df_cleaned) - 1):
            total_distance += int(self.df_cleaned.iloc[idx]['Distance to Next Station (km)'])
            if total_distance >= distance:
                break
            if int(self.df_cleaned.iloc[idx + 1]['Reservation Availability']) == 1:
                return 1
        return 0

    def train_model(self):
        self.df_cleaned['Label'] = [self.label_stations_within_distance(i, self.dynamic_distance) for i in range(len(self.df_cleaned))]
        X = self.df_cleaned[['Distance to Next Station (km)']]
        y = self.df_cleaned['Label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.model = SVC()
        self.model.fit(X_train_scaled, y_train)

    def check_previous_distance(self, index, distance):
        total_distance = 0
        stations_with_availability = []
        for idx in range(index - 1, -1, -1):
            total_distance += int(self.df_cleaned.iloc[idx]['Distance to Next Station (km)'])
            if total_distance >= distance:
                break
            if int(self.df_cleaned.iloc[idx]['Reservation Availability']) == 1:
                station_name = self.df_cleaned.iloc[idx]['Station Name']
                available_seats = int(self.df_cleaned.iloc[idx]['Total Seat Available'])
                stations_with_availability.append((station_name, available_seats, total_distance))
        stations_with_availability.sort(key=lambda x: (x[2], -x[1]))
        return stations_with_availability

    def check_all_stations_within_distance(self, from_index, distance):
        total_distance = 0
        stations_with_availability = []
        for idx in range(from_index, len(self.df_cleaned) - 1):
            total_distance += int(self.df_cleaned.iloc[idx]['Distance to Next Station (km)'])
            if total_distance >= distance:
                break
            if int(self.df_cleaned.iloc[idx + 1]['Reservation Availability']) == 1:
                station_name = self.df_cleaned.iloc[idx + 1]['Station Name']
                available_seats = int(self.df_cleaned.iloc[idx + 1]['Total Seat Available'])
                stations_with_availability.append((station_name, available_seats, total_distance))
        stations_with_availability.sort(key=lambda x: (x[2], -x[1]))
        return stations_with_availability

    def find_best_station(self, from_station, to_station):
        if from_station in self.df_cleaned['Station Name'].values and to_station in self.df_cleaned['Station Name'].values:
            from_idx = self.df_cleaned[self.df_cleaned['Station Name'] == from_station].index[0]
            to_idx = self.df_cleaned[self.df_cleaned['Station Name'] == to_station].index[0]

            if from_idx < to_idx and from_idx < len(self.df_cleaned) and (to_idx - 1) >= 0:
                boarding_station = self.df_cleaned.iloc[from_idx]
                available_stations = self.check_all_stations_within_distance(from_idx, self.dynamic_distance)
                previous_stations = self.check_previous_distance(from_idx, self.dynamic_distance)

                combined_stations = available_stations + previous_stations

                if combined_stations:
                    available_station_list = [
                        {
                            "train_name":"Gitanjali Express",
                            "train_number": "12860",
                            "from": station[0],  
                            "to": to_station,    
                            "availableSeats": int(station[1]),  
                            # Separate arrival day and time
                            # "from_day": int(self.df_cleaned[self.df_cleaned['Station Name'] == station[0]].iloc[0]['Day']),
                            "from_sta": self.df_cleaned[self.df_cleaned['Station Name'] == station[0]].iloc[0]['Arrives'],
                            # Separate departure day and time
                            "from_day": int(self.df_cleaned[self.df_cleaned['Station Name'] == station[0]].iloc[0]['Day']),
                            "from_std": self.df_cleaned[self.df_cleaned['Station Name'] == station[0]].iloc[0]['Departs'],
                            # Separate destination arrival day and time
                            "to_day": int(self.df_cleaned[self.df_cleaned['Station Name'] == to_station].iloc[0]['Day']),
                            "to_std": self.df_cleaned[self.df_cleaned['Station Name'] == to_station].iloc[0]['Arrives']
                        }
                        for station in combined_stations
                    ]
                else:
                    available_station_list = []
            else:
                available_station_list = []
        else:
            available_station_list = []

        return available_station_list

if __name__ == "__main__":
    system = TrainReservationSystem('Gitanjali Express Route.csv')
    available_stations = system.find_best_station('ROU', 'CSMT')
    print("Available stations (with seat count and distance):", available_stations)