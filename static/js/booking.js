// Select all "Book Now" buttons
const bookNowButtons = document.querySelectorAll("button.flex.cursor-pointer");

// Add a click event listener to each button
bookNowButtons.forEach(button => {
  button.addEventListener("click", function() {
    // Redirect to passenger.html
    window.location.href = "passenger";
  });
});