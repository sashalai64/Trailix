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