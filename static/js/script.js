function openLoginPage() {
    window.location.href = 'login';
}

document.getElementById('ticketForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const fromStation = document.getElementById('from').value;
    const toStation = document.getElementById('to').value;
    const travelDate = document.getElementById('travelDate').value;
    const bookingType = document.getElementById('bookingType').value;
    const classType = document.getElementById('classType').value;

    window.location.href = 'trains';
});
