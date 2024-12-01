

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('form');
    const placeInput = document.getElementById('place');

    searchForm.addEventListener('submit', function(event) {
        if (!placeInput.value.trim()) {
            alert("Please enter a valid location to search for cafes.");
            event.preventDefault(); // Prevent form submission if input is invalid
        }
    });
});
