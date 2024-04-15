// Add an event listener for the popstate event (back navigation)
window.addEventListener('popstate', function (event) {
    // Reload the page when the back button is pressed
    location.reload();
});