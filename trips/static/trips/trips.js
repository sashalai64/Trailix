const currentPageType = typeof pageType !== 'undefined' ? pageType : null;

// Get countdown for upcoming trips
if (currentPageType === 'upcoming-trips'){
    document.addEventListener('DOMContentLoaded', function() {
        function startCountdown() {
            const trips = document.querySelectorAll('[data-trip-id]');

            trips.forEach(tripElement => {
                const tripId = tripElement.getAttribute('data-trip-id');
                const startDate = tripElement.getAttribute('data-trip-start');
                const rawOffset = parseInt(tripElement.getAttribute('data-raw-offset'), 10) || 0; // Default offset as 0

                // Log the startDate and countDownDate
                console.log(`Trip ID: ${tripId}`);
                console.log(`Start Date (raw): ${startDate}`);
                console.log(`Offset Time: ${rawOffset}`);

                if (!startDate || isNaN(rawOffset)) {
                    console.error(`Invalid start date or offset for trip ID: ${tripId}`);
                    return;
                }
        
                // Adjust start date to local time using raw offset
                const countDownDate = new Date(new Date(startDate).getTime() + rawOffset * 1000);
                console.log(`Countdown Date (timestamp): ${countDownDate}`);

                function updateCountdown() {
                    const now = new Date().getTime();
                    const distance = countDownDate.getTime() - now;

                    if (distance > 0) {
                        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

                        document.getElementById(`countdown-${tripId}`).innerText = 
                            `${days}d ${hours}h ${minutes}m ${seconds}s`;
                    } else {
                        document.getElementById(`countdown-${tripId}`).innerText = 'Trip Started!';
                    }
                }

                // Initial call to updateCountdown and interval to update every second
                updateCountdown();
                setInterval(updateCountdown, 1000);
            });
        }
        startCountdown();
    });
}


// Autocomplete for city in forms.py
$(document).ready(function() {
    // Disable the submit button initially until the user selects a city from autocomplete
    $('#submit-button').prop('disabled', true);

    $('#city-input').autocomplete({
        source: function(request, response) {
            var countryCode = $('#country-input').val();
            var query = request.term;

            // Check if country code is provided
            if (!countryCode) {
                console.error("Country code is missing");
                return;
            }

            $.ajax({
                url: `/get-cities/`,
                data: {
                    country_code: countryCode,
                    query: query
                },
                method: 'GET',
                success: function(responseData) {
                    console.log(responseData);
                    
                    // Populate the cities array with city names from the response
                    if (responseData && responseData.data && Array.isArray(responseData.data)){
                        let cities = [];
                        responseData.data.forEach(function(city) {
                            cities.push({
                                label: city.name,
                                value: city.name,
                                wikiId: city.wikiDataId,
                                lat: city.latitude, 
                                lng: city.longitude 
                            });
                        });
                        response(cities);
                    } else {
                        console.error("Expected an array but got:", responseData);
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching cities:", error);
                }
            });
        },
        minLength: 3,
        delay: 200,
        select: function(event, ui) {
            // Set the selected value to the input fields
            $('#city-input').val(ui.item.value);
            $('#wikiId-input').val(ui.item.wikiId);
            $('#lat-input').val(ui.item.lat);
            $('#lng-input').val(ui.item.lng);

            console.log("Longitude:", ui.item.lat);
            console.log("Latitude:", ui.item.lng);
            console.log("wikiId:", ui.item.wikiId);

            // Enable the submit button since a city has been selected
            $('#submit-button').prop('disabled', false);

            return false;
        }
    });

    // Re-disable the submit button if the user clears the input
    $('#city-input').on('input', function() {
        if ($(this).val().trim() === '') {
            $('#submit-button').prop('disabled', true);

            // clear the hidden fields if necessary
            $('#wikiId-input').val('');
            $('#lat-input').val('');
            $('#lng-input').val('');
        }
    });
});


//Update local time without refreshing the page
document.addEventListener('DOMContentLoaded', function() {
    function updateLocalTime(tripId, rawOffset) {
        const now = new Date();
        const localTime = new Date(now.getTime() + (rawOffset * 1000));

        //Update the local time display
        document.getElementById(`local-time-${tripId}`).innerText = localTime.toLocaleString();
    }

    function startUpdatingLocalTimes() {
        const trips = document.querySelectorAll('[data-trip-id]');

        trips.forEach(tripElement => {
            const tripId = tripElement.getAttribute('data-trip-id');
            const rawOffset = parseInt(tripElement.getAttribute('data-raw-offset'), 10);

            // Log the startDate and Offset
            console.log(`Trip ID: ${tripId}`);
            console.log(`Offset Time: ${rawOffset}`);

            //Fetch and update the local time initially
            if (!isNaN(rawOffset)) {
                updateLocalTime(tripId, rawOffset);
            }

            //Set up periodic updates every second
            setInterval(() => {
                if (!isNaN(rawOffset)) {
                    updateLocalTime(tripId, rawOffset);
                }
            }, 1000);
        });
    }

    //Initial call to start updating local times
    startUpdatingLocalTimes();
});


// Create a Leaflet map for previous trips
if (currentPageType === 'previous-trips'){
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize the map
        var map = L.map('map').setView([0, 0], 2) // Set default view to world map

        // Add a tile layer
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        // Extract JSON data from the script tag
        const tripsDataScript = document.getElementById('trips-data');
        let trips = []

        if (tripsDataScript) {
            try {
                trips = JSON.parse(tripsDataScript.textContent);
                console.log('Data from views.py:', trips);
                // Use the data in your JavaScript logic
            } catch (error) {
                console.error('Failed to parse JSON:', error);
            }
        } else {
            console.error('Data script tag not found.');
        }

        // Check if trips data is available
        if (trips.length > 0) {
            // Create a bounds object to fit all markers
            var bounds = [];

            // Add markers for each trip
            trips.forEach(trip => {
                const { city, country, lat, lng } = trip.fields;

                if (lat && lng){
                    // Add marker to the map
                    const marker = L.marker([lat, lng]).addTo(map);

                    // Add popup with trip details
                    marker.bindPopup(`<b>${city}, ${country}</b><br>Visited on ${trip.fields.start_date}`);

                    // Extend the bounds to include this marker
                    bounds.push([lat, lng]);
                } else{
                    console.warn(`Invalid coordinates for trip: ${trip.pk}`);
                }
            });

            // Adjust the map to fit all markers
            if (bounds.length > 0) {
                map.fitBounds(bounds);
            } else {
                console.error('No trips data available.');
            } 
        } else {
            console.error('No trips data available.');
        }
    });
}