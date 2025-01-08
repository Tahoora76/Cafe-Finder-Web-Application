document.getElementById("search-button").addEventListener("click", async function () {
    const location = document.getElementById("location").value;

    if (!location) {
        alert("Please enter a location.");
        return;
    }

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ location })
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Response from server:", data);
            checkResults();
        } else {
            const error = await response.json();
            console.error("Error from server:", error);
            alert("Failed to start scraping: " + error.error);
        }
    } catch (err) {
        console.error("Error in fetch:", err);
        alert("Failed to start scraping. Please try again.");
    }
});
