(() => {

    document.addEventListener('DOMContentLoaded', function () {
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        // Payment Method Selection
        const methodCards = document.querySelectorAll('.payment-method-card');
        const methodInput = document.getElementById('paymentMethod');
        const methodError = document.getElementById('methodError');

        methodCards.forEach(card => {
            card.addEventListener('click', function () {
                // Remove selected state from all
                methodCards.forEach(c => c.classList.remove('selected'));
                // Add to clicked
                this.classList.add('selected');
                // Update hidden input
                methodInput.value = this.dataset.method;
                // Clear error
                if (methodError) methodError.style.display = 'none';
            });

            // Keyboard accessibility
            card.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        });

        // Form Validation & Submission
        const form = document.getElementById('depositForm');
        const amountInput = document.getElementById('amount');
        const amountError = document.getElementById('amountError');
        const submitBtn = document.getElementById('submitBtn');
        const submitSpinner = document.getElementById('submitSpinner');
        const submitText = document.getElementById('submitText');

        // Real-time amount validation
        amountInput.addEventListener('input', function () {
            const value = parseFloat(this.value);
            if (this.value && (isNaN(value) || value < 10 || value > 50000)) {
                this.classList.add('is-invalid');
                if (amountError) amountError.style.display = 'block';
            } else {
                this.classList.remove('is-invalid');
                if (amountError) amountError.style.display = 'none';
            }
        });

        // Form submit handler
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            let isValid = true;

            // Validate payment method
            if (!methodInput.value) {
                if (methodError) methodError.style.display = 'block';
                isValid = false;
            }

            // Validate amount
            const amount = parseFloat(amountInput.value);
            if (!amountInput.value || isNaN(amount) || amount < 10 || amount > 50000) {
                amountInput.classList.add('is-invalid');
                if (amountError) amountError.style.display = 'block';
                isValid = false;
            }

            if (!isValid) return;

            // Show loading state
            submitBtn.disabled = true;
            submitSpinner.classList.remove('d-none');
            submitText.textContent = 'Processing...';

            // Simulate form submission (replace with actual fetch/axios call)
            setTimeout(() => {
                // For demo: show success message
                alert(`✓ Deposit request submitted!\n\nMethod: ${methodInput.value}\nAmount: $${amount.toFixed(2)}`);

                // Reset form
                form.reset();
                methodCards.forEach(c => c.classList.remove('selected'));
                methodInput.value = '';

                // Restore button
                submitBtn.disabled = false;
                submitSpinner.classList.add('d-none');
                submitText.textContent = 'Proceed to Deposit';

                // In production, redirect or update UI:
                // window.location.href = '/dashboard/deposits/confirmation';
            }, 1500);
        });

        // Auto-hide alerts after 5 seconds (if you add alert functionality later)
        window.hideAlert = function (alertId) {
            const alert = document.getElementById(alertId);
            if (alert) {
                alert.classList.add('fade');
                setTimeout(() => alert.remove(), 300);
            }
        };
    });
})();