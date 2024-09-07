#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

data = pd.read_csv('Gitanjali Express Route.csv')
data


# In[2]:


df_cleaned = pd.DataFrame(data)
df_cleaned = df_cleaned.drop(columns=['Arrives', 'Departs', 'Stop Time(MIN)'])
df_cleaned


# In[4]:


def label_stations_within_250_km(index):
    total_distance = 0
    for idx in range(index, len(df_cleaned) - 1):
        total_distance += df_cleaned.iloc[idx]['Distance to Next Station (km)']
        if total_distance >= 250:
            break
        if df_cleaned.iloc[idx + 1]['Reservation Availability'] == 1:
            return 1
    return 0

df_cleaned['Label'] = [label_stations_within_250_km(i) for i in range(len(df_cleaned))]

X = df_cleaned[['Distance to Next Station (km)']]
y = df_cleaned['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = SVC()
model.fit(X_train_scaled, y_train)

def predict_reservation_within_250_km(distance):
    scaled_distance = scaler.transform(pd.DataFrame([[distance]], columns=['Distance to Next Station (km)']))
    prediction = model.predict(scaled_distance)
    return prediction[0] == 1

def check_previous_250_km(index):
    total_distance = 0
    available_stations = []
    for idx in range(index - 1, -1, -1):
        total_distance += df_cleaned.iloc[idx]['Distance to Next Station (km)']
        if total_distance >= 250:
            break
        if df_cleaned.iloc[idx]['Reservation Availability'] == 1:
            available_stations.append(df_cleaned.iloc[idx]['Station Name'])
    return available_stations

from_station = input("Enter Boarding Station: ").strip().upper()
to_station = input("Enter Destination: ").strip().upper()

if from_station in df_cleaned['Station Name'].values and to_station in df_cleaned['Station Name'].values:
    from_idx = df_cleaned[df_cleaned['Station Name'] == from_station].index[0]
    to_idx = df_cleaned[df_cleaned['Station Name'] == to_station].index[0]
    
    if from_idx < to_idx and from_idx < len(df_cleaned) and (to_idx - 1) >= 0:
        available_stations = []
        total_distance = 0
        
        for idx in range(from_idx, min(to_idx, len(df_cleaned) - 1)):
            distance = df_cleaned.iloc[idx]['Distance to Next Station (km)']
            if total_distance + distance >= 250:
                break
            total_distance += distance
            if df_cleaned.iloc[idx + 1]['Reservation Availability'] == 1:
                if predict_reservation_within_250_km(df_cleaned.iloc[idx + 1]['Distance to Next Station (km)']):
                    available_stations.append(df_cleaned.iloc[idx + 1]['Station Name'])
        
        previous_stations = check_previous_250_km(from_idx)
        
        if available_stations:
            print(f"Stations with available reservations within 250 km from {from_station}: {', '.join(available_stations)}")
        else:
            print("No stations with available reservations within 250 km in the specified range.")
        
        if previous_stations:
            print(f"Stations with available reservations within 250 km before {from_station}: {', '.join(previous_stations)}")
        else:
            print(f"No stations with available reservations within 250 km before {from_station}.")
    else:
        print("Invalid range of stations.")
else:
    print("Invalid station names provided.")


# In[ ]:




