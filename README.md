
# IRCTC Smart Train Reservation System

The Smart Train Reservation System by IRCTC aims to enhance the traditional booking process by introducing a more user-friendly seat selection system. This system allows users to select their desired seats based on criteria such as age groups and proximity to other passengers, along with providing a visual representation of the available seats.Furthermore, the system includes a feature for dynamic seat pricing, adjusting costs based on seat availability, and utilizes machine learning clustering to recommend seats based on user preferences.

The system permits users to choose their originating and destination stations while checking the availability of seats from the originating station. If there are no seats available, it provides alternative stations within a flexible range of 200-250 km, which adapts depending on whether it is a holiday or weekend. Utilizing an SVM classifier, a machine learning model categorizes stations based on seat availability and forecasts future availability by adjusting features such as "Distance to Next Station" to ensure accuracy. When no seats are available from the selected station, the system suggests nearby stations with open reservations, prioritizing them based on proximity and seat availability, considering both preceding and succeeding stations from the originating point.


## Technology Used

- Frontend:
HTML/CSS for visual seat selection interface.
JavaScript for dynamic interaction and user inputs.

- Backend:
Python with machine learning libraries (e.g., scikit-learn, numpy) for clustering and seat recommendation.
Flask for server-side operations.

- Machine Learning:
SVM (Support Vector Machine): Used for station classification and seat availability prediction.
Clustering Models: Recommends seats based on passenger preferences.


## Features

- Provides nearby stations within 200-250 km when no seats are available, adapting to holidays and weekends. Recommendations for both preceding and succeeding stations from the originating point.
- Visual representation of available and booked seats. Seat selection based on age group and proximity to other passengers.






