// Select all "Book Now" buttons



async function fetchTrainDetails() {
  const from = document.getElementById("from").value;
  const to = document.getElementById("to").value;
  const journeyDate = document.getElementById("journeyDate").value;

  try {
    const response = await fetch('/get_trains', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ from, to, journeyDate })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const trainDetails = await response.json();
    console.log('API Response:', trainDetails);  // Log the full response

    if (trainDetails && trainDetails.status === true && trainDetails.data) {
      displayTrainDetails(trainDetails.data);
    } else {
      document.getElementById("train_details").innerHTML = `<p>No trains found or invalid data format.</p>`;
    }
  } catch (error) {
    console.error('Error fetching train details:', error);
    document.getElementById("train_details").innerHTML = `<p>Error fetching train details: ${error.message}</p>`;
  }
}

function displayTrainDetails(trainsData) {
  const trainDetailsDiv = document.getElementById("train_details");

  // Clear previous train details if any
  trainDetailsDiv.innerHTML = '';

  if (!trainsData || trainsData.length === 0) {
    trainDetailsDiv.innerHTML = `<p>No trains found.</p>`;
    return;
  }

  let trains = '';
  trainsData.forEach(train => {
    trains += `<div class="train-card bg-white shadow-md rounded-lg p-6 mb-4">
                    <h3 class="train-name text-lg font-bold text-gray-800 mb-2">${train.train_name} (${train.train_number})</h3>
                    <div class="train-info flex justify-between items-center border-t border-b border-gray-200 py-2 my-2">
                        <div class="info-item text-center">
                            <p class="label text-sm font-medium text-gray-500">Departure:</p>
                            <p class="value text-lg font-semibold text-gray-700">${train.from_sta} at ${train.from_std}</p>
                        </div>
                        <div class="info-item text-center">
                            <p class="label text-sm font-medium text-gray-500">Arrival:</p>
                            <p class="value text-lg font-semibold text-gray-700">${train.to_sta} at ${train.to_std}</p>
                        </div>
                        <div class="info-item text-center">
                            <p class="label text-sm font-medium text-gray-500">Duration:</p>
                            <p class="value text-lg font-semibold text-gray-700">${train.duration}</p>
                        </div>
                    </div>
                    <div class="station-info flex justify-between items-center py-2">
                        <div class="station text-center">
                            <p class="label text-sm font-medium text-gray-500">From:</p>
                            <p class="value text-lg font-semibold text-gray-700">${train.from_station_name}</p>
                        </div>
                        <div class="station text-center">
                            <p class="label text-sm font-medium text-gray-500">To:</p>
                            <p class="value text-lg font-semibold text-gray-700">${train.to_station_name}</p>
                        </div>
                    </div>
                    <div class="additional-info flex justify-between items-center py-2">
                        <div class="distance text-center">
                            <p class="label text-sm font-medium text-gray-500">Distance:</p>
                            <p class="value text-lg font-semibold text-gray-700">${train.distance} km</p>
                        </div>
                        <div class="train-type text-center">
                            <p class="label text-sm font-medium text-gray-500">Train Type:</p>
                            <p class="value text-lg font-semibold text-gray-700">${train.train_type}</p>
                        </div>
                    </div>
                    <div class="availability py-2 text-center">
                        <p class="status ${train.availableSeats > 0 ? 'text-green-600' : 'text-red-600'}">
                            ${train.availableSeats > 0 ? `Available: ${train.availableSeats} Seats` : 'Waitlisted'}
                        </p>
                    </div>
                    <button class="book-btn bg-blue-500 text-white py-2 px-4 rounded-lg w-full font-bold mt-4 hover:bg-blue-600">
                        Book Now
                    </button>
                 </div>`;
  });

  // Append the generated train details HTML to the trainDetailsDiv
  trainDetailsDiv.innerHTML = trains;

  const bookNowButtons = document.querySelectorAll('.book-btn');

  // Add a click event listener to each button
  bookNowButtons.forEach(button => {
    button.addEventListener("click", function () {
      // Redirect to passenger.html
      window.location.href = "passenger";
    });
  });

}
