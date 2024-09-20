function generatePNR() {
    let pnr = '';
    for (let i = 0; i < 10; i++) {
        pnr += Math.floor(Math.random() * 10);
    }
    return pnr;
}

function getRandomCoach(coaches) {
    const randomIndex = Math.floor(Math.random() * coaches.length);
    return coaches[randomIndex];
}

// Retrieve train and passenger details from localStorage
document.addEventListener("DOMContentLoaded", function () {
    const selectedTrain = JSON.parse(localStorage.getItem('selectedTrain'));
    const trainDetails = `(${selectedTrain.train_number})`;
    const trainName = `${selectedTrain.train_name}`;
    const pnrNumber = generatePNR();

    // Get passenger details from local storage
    const passengerDetailsArray = JSON.parse(localStorage.getItem('passengerDetails')) || [];
    const seatNumber = localStorage.getItem('selected_seat');
    const coaches = ['Coach A', 'Coach B', 'Coach C', 'Coach D', 'Coach E'];
    const coach = getRandomCoach(coaches);

    // Display journey details
    if (trainDetails && trainName && pnrNumber) {
        document.getElementById("journeyDetails").innerText = trainDetails;
        document.getElementById("trainName").innerText = trainName;
        document.getElementById("pnrNumber").innerText = `PNR: ${pnrNumber}`;
    }

    // Display passenger details
    const passengerDetailsContainer = document.getElementById('passengerDetailsContainer');
    if (passengerDetailsArray.length > 0) {
        passengerDetailsArray.forEach(passenger => {
            const passengerDiv = document.createElement('div');
            passengerDiv.className = 'flex items-center gap-4 bg-white px-4 min-h-[72px] py-2 justify-between';
            passengerDiv.innerHTML = `
        <div class="flex items-center gap-4">
          <div class="text-[#111418] flex items-center justify-center rounded-lg bg-[#f0f2f4] shrink-0 size-12"
            data-icon="Person" data-size="24px" data-weight="regular">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor"
              viewBox="0 0 256 256">
              <path
                d="M208,136H176V104h16a16,16,0,0,0,16-16V40a16,16,0,0,0-16-16H64A16,16,0,0,0,48,40V88a16,16,0,0,0,16,16H80v32H48a16,16,0,0,0-16,16v16a16,16,0,0,0,16,16h8v40a8,8,0,0,0,16,0V184H184v40a8,8,0,0,0,16,0V184h8a16,16,0,0,0,16-16V152A16,16,0,0,0,208,136ZM64,40H192V88H64Zm32,64h64v32H96Zm112,64H48V152H208v16Z">
              </path>
            </svg>
          </div>
          <div class="flex flex-col justify-center">
            <p class="text-[#111418] text-base font-medium leading-normal line-clamp-1">${passenger.full_name}</p>
            <p class="text-[#637588] text-sm font-normal leading-normal line-clamp-2">Age: ${passenger.age}</p>
          </div>
        </div>
      `;
            passengerDetailsContainer.appendChild(passengerDiv);
        });
    }

    // Display seat details
    if (seatNumber && coach) {
        document.getElementById("seatDetails").innerText = `Seat: ${seatNumber}, Coach: ${coach}`;
        window.onpopstate = function (event) {
            // Redirect to a different page if the user tries to navigate back
            window.location.replace('/');
        };
    }
});

function goToHome() {
    window.location.href = '/';
}

