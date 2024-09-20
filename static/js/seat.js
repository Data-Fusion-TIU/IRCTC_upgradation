var count = 0;
var selectedSeatsList = []; // List to store the selected seat numbers

function selectSeat(seatNumber) {
    const selectedSeatInput = document.getElementById('selectedSeatInput');
    const passengerDetails = JSON.parse(localStorage.getItem('passengerDetails')) || [];
    const passengerNum = passengerDetails.length;

    // Check if the seat is already selected
    if (selectedSeatsList.includes(seatNumber)) {
        // Remove the seat number from the list if it's already selected
        selectedSeatsList = selectedSeatsList.filter(seat => seat !== seatNumber);
        count -= 1;  // Decrease count when a seat is deselected

        // Toggle the selected class on the seat element
        const seatElement = document.getElementById('seat-' + seatNumber);
        seatElement.classList.remove('selected');
    } else {
        // Check if selected seats exceed the passenger number
        if (count >= passengerNum) {
            alert("Seat cannot be selected more than the number of passengers");
        } else {
            // Add the seat number to the list if it's not already selected
            selectedSeatsList.push(seatNumber);
            count += 1;  // Increment count when a seat is selected

            // Update the selectedSeatInput value to reflect the current seat selection list
            selectedSeatInput.value = selectedSeatsList.join(',');

            // Toggle the selected class on the seat element
            const seatElement = document.getElementById('seat-' + seatNumber);
            seatElement.classList.add('selected');
        }
    }
}

function bookSeat() {
    const selectedSeat = document.getElementById('selectedSeatInput').value;
    const modal = document.getElementById('modal');
    const modalMessage = document.getElementById('modal-message');
    
    if (selectedSeat) {
        // Save the selected seat to local storage
        localStorage.setItem('selected_seat', selectedSeat);

        // Show the custom alert (modal)
        modalMessage.innerText = "You have booked seat number: " + selectedSeat;
        modal.style.display = "block";

        // Redirect to the pay_and_confirm page after a delay
        setTimeout(() => {
            window.location.href = "/pay_and_confirm";
        }, 2000); // Adjust delay as needed
    } else {
        // Show the custom alert for no seat selected
        modalMessage.innerText = "Please select a seat.";
        modal.style.display = "block";
        setTimeout(() => {
            modal.style.display = "none";
        }, 2000); // Adjust delay as needed
    }
}

// Close the modal when the user clicks on <span> (x)
const closeModal = document.getElementById('modal-close');
closeModal.onclick = function () {
    document.getElementById('modal').style.display = "none";
}

// Close the modal if the user clicks anywhere outside of the modal
window.onclick = function (event) {
    if (event.target == document.getElementById('modal')) {
        document.getElementById('modal').style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the stored train details from localStorage
    const selectedTrain = JSON.parse(localStorage.getItem('selectedTrain'));

    if (selectedTrain) {
        // Display the train details on the passenger page
        document.getElementById("train_name").textContent = `Train Name: ${selectedTrain.train_name} (${selectedTrain.train_number})`;
        document.getElementById("from_sta").textContent = `${selectedTrain.from_sta} at ${selectedTrain.from_std}`;
        document.getElementById("to_sta").textContent = `${selectedTrain.to_sta} at ${selectedTrain.to_std}`;
        document.getElementById("distance").textContent = `Distance: ${selectedTrain.distance} km`;
        document.getElementById("availableSeats").textContent = `Available Seats: ${selectedTrain.availableSeats}`;
    } else {
        document.getElementById("train_info").textContent = "No train details found. Please go back and select a train.";
    }

    // Retrieve passenger details from localStorage
    const passengerDetails = JSON.parse(localStorage.getItem('passengerDetails')) || [];

    if (passengerDetails.length > 0) {
        // Create a list to display all passenger details
        const passengerList = document.getElementById("passenger-list");
        passengerDetails.forEach((passenger, index) => {
            const passengerItem = document.createElement('li');
            passengerItem.textContent = `Passenger ${index + 1}: ${passenger.name}, Age: ${passenger.age}, Phone: ${passenger.phone}, Gender: ${passenger.gender}`;
            passengerList.appendChild(passengerItem);
        });
    } else {
        // Handle the case where no passenger details are found
        document.getElementById("passenger-list").textContent = 'No passengers added.';
    }
});
