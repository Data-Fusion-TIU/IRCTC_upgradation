const ticketBookingDiv = document.querySelector(".flex.flex-1.gap-3.rounded-lg.border.bg-slate-50");

ticketBookingDiv.addEventListener("click", function() {
  window.location.href = "booking";
});



const registerButton = document.getElementById("registerbtn");

const signInButton = document.getElementById("signinbtn");


registerButton.addEventListener("click", function() {
  window.location.href = "signup"; 
});

signInButton.addEventListener("click", function() {
  window.location.href = "signin"; 
});

// Get the modal
var modal = document.getElementById("contactModal");

// Get the button that opens the modal
var btn = document.getElementById("contactUsBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
