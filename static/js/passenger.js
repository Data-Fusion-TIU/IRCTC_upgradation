let passengerCount = 0;
let passengerDetailsArray = [];

function addPassengerDetails(event) {
    event.preventDefault();  // Prevent the default form submission

    const passengerList = document.getElementById('passenger-list');  // Ensure the element is found after DOM is loaded

    const fullName = document.getElementById("full_name").value;
    const age = document.getElementById("age").value;
    const phone = document.getElementById("phone").value;
    const gender = document.getElementById("gender").value;
    const ageGroup = document.getElementById("age_group").value;

    if (passengerCount < 6) {
        // Create passenger object
        const passengerDetails = {
            full_name: fullName,
            age: age,
            phone: phone,
            gender: gender,
            age_group: ageGroup
        };

        // Add passenger details to array and store in localStorage
        passengerDetailsArray.push(passengerDetails);
        localStorage.setItem('passengerDetails', JSON.stringify(passengerDetailsArray));

        // Append passenger details to the UI
        const passengerHTML = `
      <div class="flex flex-col border border-gray-300 p-4 rounded-lg bg-white">
        <h3 class="text-lg font-semibold">Passenger ${passengerCount + 1}</h3>
        <p class="text-gray-700">Name: ${fullName}</p>
        <p class="text-gray-700">Age: ${age}</p>
        <p class="text-gray-700">Sex: ${gender}</p>
      </div>
    `;
        passengerList.insertAdjacentHTML('beforeend', passengerHTML);  // Now it will find the element correctly
        passengerCount++;

        // Clear form fields
        document.getElementById("full_name").value = '';
        document.getElementById("age").value = '';
        document.getElementById("phone").value = '';
        document.getElementById("gender").value = '';
        document.getElementById("age_group").value = '';
    } else {
        alert('Maximum 6 passengers allowed!');
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the stored train details from localStorage
    const selectedTrain = JSON.parse(localStorage.getItem('selectedTrain'));

    if (selectedTrain) {
        // Display the train details on the passenger page (you can customize this part)
        document.getElementById("train_name").textContent = `Train Name: ${selectedTrain.train_name} (${selectedTrain.train_number})`;
        document.getElementById("from_sta").textContent = `${selectedTrain.from} at ${selectedTrain.from_std}`;
        document.getElementById("to_sta").textContent = `${selectedTrain.to} at ${selectedTrain.to_std}`;
        document.getElementById("distance").textContent = `Distance: ${selectedTrain.distance} km`;
        document.getElementById("availableSeats").textContent = `Available Seats: ${selectedTrain.availableSeats}`;
    } else {
        document.getElementById("train_info").textContent = "No train details found. Please go back and select a train.";
    }
    document.getElementById("continueButton").addEventListener("click", function (event) {
        event.preventDefault();  // Prevent the default form submission

        // Get the passenger details from localStorage
        const storedPassengers = JSON.parse(localStorage.getItem('passengerDetails')) || [];

        if (storedPassengers.length > 0) {
            // Create a form element to submit the data
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/seat';  // Set the action to your Flask route or desired route

            // Add each passenger as a hidden input field
            storedPassengers.forEach((passenger, index) => {
                for (const [key, value] of Object.entries(passenger)) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = `passenger${index + 1}_${key}`;
                    input.value = value;
                    form.appendChild(input);
                }
            });

            document.body.appendChild(form);
            form.submit();
        } else {
            alert('Please add at least one passenger before continuing.');
        }
    });
});

