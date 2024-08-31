// Get countdown for upcoming trips
document.addEventListener('DOMContentLoaded', function() {
    function startCountdown() {
        const trips = document.querySelectorAll('[data-trip-id]');

        trips.forEach(tripElement => {
            const tripId = tripElement.getAttribute('data-trip-id');
            const startDate = tripElement.getAttribute('data-trip-start');
            const countDownDate = new Date(startDate).getTime();

            function updateCountdown() {
                const now = new Date().getTime();
                const distance = countDownDate - now;

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

// Autocomplete for city in forms.py
$(document).ready(function() {
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
                    let cities = [];
                    responseData.data.forEach(function(city) {
                        cities.push(city.name);
                    });

                    // Send the cities array to the autocomplete
                    response(cities);
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching cities:", error);
                }
            });
        },
        minLength: 3,
        delay: 200,
        select: function(event, ui) {
            // Set the selected value to the city input field
            $('#city-input').val(ui.item.value);
            return false;
        }
    });
});