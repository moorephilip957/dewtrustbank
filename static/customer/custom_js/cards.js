(() => {
    // View card details
    function viewCard(cardId) {
        // In production, fetch card details from API
        // For demo, show modal with placeholder data
        const modal = new bootstrap.Modal(document.getElementById('viewCardModal'));

        // Populate with demo data (replace with API call)
        document.getElementById('modalCardNumber').textContent = '•••• •••• •••• 1234';
        document.getElementById('modalCardExpiry').textContent = '12/25';
        document.getElementById('modalCardName').textContent = 'Andrew Levin';
        document.getElementById('modalCardFullNumber').textContent = '4532 •••• •••• 1234';

        modal.show();
    }

    // Manage card (edit settings, limits, etc.)
    function manageCard(cardId) {
        window.location.href = `${cardId}/`;
    }

    // Copy to clipboard
    function copyToClipboard(text, btn) {
        navigator.clipboard.writeText(text).then(() => {
            const icon = btn.querySelector('i');
            icon.className = 'bi bi-check-lg text-success';
            setTimeout(() => {
                icon.className = 'bi bi-clipboard';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
            alert('Failed to copy to clipboard');
        });
    }

    // Show/hide CVV
    function showCVV(btn) {
        const icon = btn.querySelector('i');
        if (icon.className.includes('eye')) {
            icon.className = 'bi bi-eye-slash';
            btn.nextElementSibling.textContent = '123'; // Demo CVV
        } else {
            icon.className = 'bi bi-eye';
            btn.nextElementSibling.textContent = '•••';
        }
    }

    // Freeze card action
    function freezeCard() {
        if (confirm('Are you sure you want to freeze this card? It will be temporarily disabled for all transactions.')) {
            // In production, make API call to freeze card
            alert('Card has been frozen. You can unfreeze it anytime from card settings.');
            bootstrap.Modal.getInstance(document.getElementById('viewCardModal')).hide();
        }
    }

    // Initialize Bootstrap components
    document.addEventListener('DOMContentLoaded', function () {
        // Auto-initialize any tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    });
})();