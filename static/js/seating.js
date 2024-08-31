document.addEventListener('DOMContentLoaded', () => {
    const seats = document.querySelectorAll('.seat');
    const submitButton = document.getElementById('submit-seats');

    seats.forEach(seat => {
        seat.addEventListener('click', () => {
            if (seat.classList.contains('available')) {
                seat.classList.toggle('selected');
            }
        });
    });

    submitButton.addEventListener('click', () => {
        const selectedSeats = [...document.querySelectorAll('.seat.selected')].map(seat => seat.getAttribute('data-seat'));
        alert(`Selected seats: ${selectedSeats.join(', ')}`);
        // Here, you can handle the selected seats, e.g., send them to a server
    });
});
