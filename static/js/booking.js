// Station mapping dictionary
const stationMapping = {
  "howrah": "HWH",
  "kharagpur": "KGP",
  "tatanagar": "TATA",
  "chakradharpur": "CKP",
  "rourkela": "ROU",
  "jharsuguda": "JSG",
  "raigarh": "RIG",
  "bilaspur": "BSP",
  "raipur": "R",
  "durg": "DURG",
  "raj Nandgaon": "RJN",
  "gondia": "G",
  "bhandara": "BRD",
  "nagpur": "NGP",
  "wardha": "WR",
  "badnera": "BD",
  "akola": "AK",
  "shegaon": "SEG",
  "malkapur": "MKU",
  "bhusaval": "BSL",
  "jalgaon": "JL",
  "nasik": "NK",
  "igatpuri": "IGP",
  "kalyan": "KYN",
  "dadar": "DR",
  "mumbai CSMT": "CSMT"
  // Add more station mappings as needed
};

function getStationCode(stationName) {
  const code = stationMapping[stationName];
  if (code) {
      return code;
  } 
  // else {
     // alert("Station not found: " + stationName);
      // return null;
  //}
    // If the station is already in code format (e.g., HWH), return as is
  return stationName.toUpperCase();
}


// Function to fetch train details and display them
async function fetchTrainDetails() {
  let from = document.getElementById("from").value;
  let to = document.getElementById("to").value;
  const journeyDate = document.getElementById("journeyDate").value;

  from = getStationCode(from);
  to = getStationCode(to);

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

    if (trainDetails && trainDetails.status === true && Array.isArray(trainDetails.data)) {
      displayTrainDetails(trainDetails.data);
    } else {
      document.getElementById("train_details").innerHTML = `<p>No trains found or invalid data format.</p>`;
    }
  } catch (error) {
    console.error('Error fetching train details:', error);
    document.getElementById("train_details").innerHTML = `<p>Error fetching train details: ${error.message}</p>`;
  }
}
// Function to display train details
async function displayTrainDetails(trainsData) {
  const trainDetailsDiv = document.getElementById("train_details");

  // Clear previous train details if any
  trainDetailsDiv.innerHTML = '';

  if (!Array.isArray(trainsData) || trainsData.length === 0) {
    trainDetailsDiv.innerHTML = `<p class="text-center text-gray-500">No trains found.</p>`;
    return;
  }

  let trainsHtml = '';
  trainsData.forEach((train, index) => {
    trainsHtml += `
      <div class="train-card bg-white shadow-lg rounded-lg p-6 mb-6 border border-gray-200" data-train-index="${index}">
        <h3 class="train-name text-2xl font-bold text-gray-800 mb-4">${train.train_name} (${train.train_number})</h3>
        <div class="train-info grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-gray-300 pt-4 mt-4">
          <div class="info-item text-center">
            <p class="label text-sm font-medium text-gray-500">Departure:</p>
            <p class="value text-lg font-semibold text-gray-700">${train.from_day + 1} ${train.from_sta}</p>
          </div>
          <div class="info-item text-center">
            <p class="label text-sm font-medium text-gray-500">Arrival:</p>
            <p class="value text-lg font-semibold text-gray-700">${train.to_day + 1} ${train.to_sta}</p>
          </div>
          <div class="info-item text-center">
            <p class="label text-sm font-medium text-gray-500">Duration:</p>
            <p class="value text-lg font-semibold text-gray-700">${train.duration}</p>
          </div>
        </div>
        <div class="station-info grid grid-cols-1 md:grid-cols-2 gap-4 py-4">
          <div class="station text-center">
            <p class="label text-sm font-medium text-gray-500">From:</p>
            <p class="value text-lg font-semibold text-gray-700">${train.from_station_name}</p>
          </div>
          <div class="station text-center">
            <p class="label text-sm font-medium text-gray-500">To:</p>
            <p class="value text-lg font-semibold text-gray-700">${train.to_station_name}</p>
          </div>
        </div>
        <div class="additional-info grid grid-cols-1 md:grid-cols-2 gap-4 py-4">
          <div class="distance text-center">
            <p class="label text-sm font-medium text-gray-500">Distance:</p>
            <p class="value text-lg font-semibold text-gray-700">${train.distance} km</p>
          </div>
          <div class="train-type text-center">
            <p class="label text-sm font-medium text-gray-500">Train Type:</p>
            <p class="value text-lg font-semibold text-gray-700">${train.train_type}</p>
          </div>
        </div>
        <div class="availability text-center py-4">
          <p class="status ${train.availableSeats > 0 ? 'text-green-600' : 'text-red-600'}">
            ${train.availableSeats > 0 ? `Available: ${train.availableSeats} Seats` : 'Waitlisted'}
          </p>
          ${train.availableSeats > 0 ? '' : `
            <button id="showNearbyStationsBtn" onclick="fetchNearbyStations('${train.from}', '${train.to}', '${index}')"
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mt-4">
              Show Nearby Stations
            </button>`}
        </div>
        <button class="book-btn bg-blue-600 text-white py-2 px-4 rounded-lg w-full font-bold mt-4 hover:bg-blue-700"
          data-train-index="${index}">
          Book Now
        </button>
      </div>`;
  });

  // Append the generated train details HTML to the trainDetailsDiv
  trainDetailsDiv.innerHTML = trainsHtml;

  const bookNowButtons = document.querySelectorAll('.book-btn');

  // Add a click event listener to each button
  bookNowButtons.forEach(button => {
    button.addEventListener("click", function () {
      const trainIndex = this.getAttribute('data-train-index');
      const selectedTrain = trainsData[trainIndex];

      // Store the selected train details in localStorage
      localStorage.setItem('selectedTrain', JSON.stringify(selectedTrain));

      // Redirect to passenger.html
      window.location.href = "passenger";
    });
  });
}


// Function to fetch nearby stations and display them
async function fetchNearbyStations(fromStation, toStation, trainIndex) {
  try {
    const response = await fetch('/get_nearby_stations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fromStation, toStation })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const nearbyStationsData = await response.json();
    console.log('Nearby Stations API Response:', nearbyStationsData);  // Debugging purpose

    if (nearbyStationsData.status && Array.isArray(nearbyStationsData.nearbyStations)) {
      displayNearbyStations(nearbyStationsData, nearbyStationsData.nearbyStations, trainIndex);
    } else {
      console.error('No nearby stations found or invalid data format');
    }
  } catch (error) {
    console.error('Error fetching nearby stations:', error);
  }
}
// Function to display nearby stations
function displayNearbyStations(nearbyStationsData, stations, trainIndex) {
  const trainCard = document.querySelector(`.train-card[data-train-index="${trainIndex}"]`);
  console.log('Train Card:', trainCard);  // Debugging purpose

  if (trainCard) {
    // Clear any existing nearby stations info
    const existingDiv = trainCard.querySelector('.nearby-stations');
    if (existingDiv) {
      existingDiv.remove();
    }

    // Check if stations is a valid array
    if (Array.isArray(stations) && stations.length > 0) {
      let stationsHtml = '<h4 class="text-sm font-bold mb-2">Nearby Stations</h4><ul>';
      stations.forEach((station, nearbyIndex) => {
        if (station && typeof station === 'object') {
          const { from, to, availableSeats, from_sta, from_std, to_std } = station;

          // Create HTML structure for each nearby station
          stationsHtml += `
            <li class="text-gray-700">
              <strong>From:</strong> ${from} | <strong>To:</strong> ${to}<br>
              <strong>Available Seats:</strong> ${availableSeats}<br>
              <strong>Departure Time:</strong> ${from_sta} - ${from_std}<br>
              <strong>Arrival Time:</strong> ${to_std}
              <button class="book-btn bg-blue-500 text-white py-2 px-4 rounded-lg w-full font-bold mt-4 hover:bg-blue-600"
                data-nearby-index="${nearbyIndex}">
                Book Now
              </button>
            </li>
            <hr class="my-2">
          `;
        } else {
          console.warn('Invalid station data:', station);  // Debugging purpose
        }
      });
      stationsHtml += '</ul>';

      const nearbyStationsDiv = document.createElement('div');
      nearbyStationsDiv.classList.add('nearby-stations');
      nearbyStationsDiv.innerHTML = stationsHtml;

      // Append nearby stations info below the "Book Now" button
      trainCard.appendChild(nearbyStationsDiv);
    } else {
      // Handle case where no stations data is available
      const noStationsDiv = document.createElement('div');
      noStationsDiv.classList.add('nearby-stations');
      noStationsDiv.innerHTML = '<p class="text-gray-700">No nearby stations available.</p>';
      trainCard.appendChild(noStationsDiv);
    }
  } else {
    console.warn(`Train card with index ${trainIndex} not found.`);  // Debugging purpose
  }

  // Add event listeners to nearby station "Book Now" buttons
  const bookNowButtons = document.querySelectorAll('.book-btn');

  bookNowButtons.forEach(button => {
    button.addEventListener("click", function () {
      const nearbyIndex = this.getAttribute('data-nearby-index');
      const nearbySelectedTrain = stations[nearbyIndex];

      // Debugging: Log the selected train index and nearbyStationsData to ensure correct data
      console.log('Nearby Station Index:', nearbyIndex);
      console.log('Nearby Station Data:', nearbySelectedTrain);

      // Store the selected train details in localStorage
      localStorage.setItem('selectedTrain', JSON.stringify(nearbySelectedTrain));

      // Redirect to passenger.html
      window.location.href = "passenger";
    });
  });
}
