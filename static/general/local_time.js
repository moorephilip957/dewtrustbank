function updateLocalTimes() {
    const elements = document.querySelectorAll('.local-time');

    elements.forEach(el => {
        const utcTime = el.getAttribute('data-utc');
        if (!utcTime) return;

        // Convert UTC string to Date
        const date = new Date(utcTime);
        const now = new Date();

        // Calculate differences
        const diffMs = now - date;
        const diffSec = Math.floor(diffMs / 1000);
        const diffMin = Math.floor(diffSec / 60);
        const diffHour = Math.floor(diffMin / 60);
        const diffDay = Math.floor(diffHour / 24);

        let displayText;

        if (diffSec < 60) {
            displayText = `${diffSec} second${diffSec !== 1 ? 's' : ''} ago`;
        } else if (diffMin < 60) {
            displayText = `${diffMin} minute${diffMin !== 1 ? 's' : ''} ago`;
        } else if (diffHour < 24) {
            displayText = `${diffHour} hour${diffHour !== 1 ? 's' : ''} ago`;
        } else if (diffDay < 7) {
            displayText = `${diffDay} day${diffDay !== 1 ? 's' : ''} ago`;
        } else {
            // Use the user's local timezone
            displayText = date.toLocaleString(undefined, {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                // timeZoneName: 'short' 
            });
        }

        el.textContent = displayText;
    });
}

// Run on page load and update every minute
document.addEventListener('DOMContentLoaded', () => {
    updateLocalTimes();
    setInterval(updateLocalTimes, 60000);
});


{/* <span class="local-time" data-utc="{{ my_datetime|date:'c' }}"></span> */}
{/* <span class="local-time" data-utc="{{ my_datetime|date:'c' }}"></span> */}