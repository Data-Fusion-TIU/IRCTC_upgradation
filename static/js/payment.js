const bookButtons = document.querySelectorAll("button");

// Add a click event listener to each button
bookButtons.forEach(button => {
    button.addEventListener("click", function () {
        const passengerDetailsArray = JSON.parse(localStorage.getItem('passengerDetails')); // Assuming an array of passengers
        const seatNumber = localStorage.getItem('selected_seat'); // Assume seat number is shared for all passengers

        // Prepare the data to be sent to the server for all passengers
        const data = {
            seatNumber: seatNumber,
            passengers: passengerDetailsArray // Send the entire array of passengers
        };

        // Send the data to the server
        fetch('/update_dataset', {
            method: 'POST', // Use POST method
            headers: {
                'Content-Type': 'application/json' // Set content type to JSON
            },
            body: JSON.stringify(data) // Convert the data to a JSON string
        })
            .then(response => {
                if (response.ok) {
                    // Redirect to success page if the request was successful
                    window.location.href = "success"; // Make sure 'success' is a valid route
                } else {
                    // Handle errors
                    console.error('Error:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
window.history.forward();
function noBack() {
    window.history.forward();
} 
