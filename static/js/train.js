// Example: Accessing seat availability and updating dynamically
/*
document.addEventListener('DOMContentLoaded', function() {
    const resultCards = document.querySelectorAll('.result-card');

    // Iterate through each result card
    resultCards.forEach(card => {
        const trainId = card.dataset.trainId;
        const seatElements = card.querySelectorAll('.train-classes .seats');

        // Display initial seat availability (can be fetched dynamically)
        seatElements.forEach(seatElement => {
            const classType = seatElement.parentElement.dataset.class;
            console.log(`Train ${trainId} - Class ${classType} has ${seatElement.textContent} seats available.`);
        });

        // Example: Updating seat availability on click (for demonstration)
        card.querySelector('.book-now').addEventListener('click', () => {
            window.location.href = 'login';
        });
    });
});*/

function gotologin(){
    window.location.href = 'book';
}
