(() => {

    document.addEventListener('DOMContentLoaded', function () {
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') lucide.createIcons();

        // ===== State =====
        const state = {
            amount: '',
            accountname: '',
            accountnumber: '',
            bankname: '',
            Accounttype: 'Online Banking',
            Description: '',
            pin: '',
            availableBalance: 0,
            isSubmitting: false
        };

        // ===== DOM Elements =====
        const amountInput = document.getElementById('amount');
        const accountnameInput = document.getElementById('accountname');
        const accountnumberInput = document.getElementById('accountnumber');
        const banknameInput = document.getElementById('bankname');
        const accounttypeSelect = document.getElementById('Accounttype');
        const descriptionInput = document.getElementById('Description');
        const pinInput = document.getElementById('pin');
        const summaryCard = document.getElementById('summaryCard');
        const previewBtn = document.getElementById('previewBtn');
        const previewModal = new bootstrap.Modal(document.getElementById('previewModal'));
        const confirmTransferBtn = document.getElementById('confirmTransferBtn');
        const confirmBtnContent = document.getElementById('confirmBtnContent');
        const confirmBtnSpinner = document.getElementById('confirmBtnSpinner');
        const confirmBtnText = document.getElementById('confirmBtnText');

        // ===== Toast Notification System =====
        function showToast(message, type = 'info', duration = 5000) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = `toast-custom ${type}`;

            const icons = { success: 'check-circle', error: 'alert-circle', warning: 'alert-triangle', info: 'info' };
            const colors = { success: '#10b981', error: '#ef4444', warning: '#f59e0b', info: '#0147E1' };

            toast.innerHTML = `
                <span class="toast-icon" style="color:${colors[type]}">
                    <i data-lucide="${icons[type]}" style="width:1.25rem;height:1.25rem;"></i>
                </span>
                <span class="toast-message">${message}</span>
                <button type="button" class="toast-close" aria-label="Close">
                    <i data-lucide="x" style="width:1rem;height:1rem;"></i>
                </button>
            `;

            container.appendChild(toast);
            if (typeof lucide !== 'undefined') lucide.createIcons();

            toast.querySelector('.toast-close').addEventListener('click', () => {
                toast.style.animation = 'slideIn 0.2s ease-in reverse';
                setTimeout(() => toast.remove(), 200);
            });

            setTimeout(() => {
                if (toast.parentNode) {
                    toast.style.animation = 'slideIn 0.2s ease-in reverse';
                    setTimeout(() => toast.remove(), 200);
                }
            }, duration);
        }

        // ===== Format Currency =====
        function formatCurrency(value) {
            return parseFloat(value || 0).toFixed(2);
        }

        // ===== Update Summary =====
        function updateSummary() {
            const amount = parseFloat(state.amount) || 0;
            const fee = 0;
            const total = amount + fee;
            const newBalance = state.availableBalance - total;

            // Update summary card
            document.getElementById('summaryAmount').textContent = formatCurrency(amount);
            document.getElementById('summaryTotal').textContent = formatCurrency(total);
            document.getElementById('newBalance').textContent = formatCurrency(newBalance);

            // Show/hide summary
            if (amount > 0) {
                summaryCard.classList.remove('hidden');
            } else {
                summaryCard.classList.add('hidden');
            }

            // Update modal preview
            document.getElementById('modalAmount').textContent = formatCurrency(amount);
            document.getElementById('modalTotal').textContent = formatCurrency(total);
            document.getElementById('modalNewBalance').textContent = formatCurrency(newBalance);
            document.getElementById('modalRecipient').textContent = state.accountname || '-';
            document.getElementById('modalAccountNumber').textContent = state.accountnumber || '-';
            document.getElementById('modalBank').textContent = state.bankname || '-';
            document.getElementById('modalAccountType').textContent = state.Accounttype;

            const descRow = document.getElementById('modalDescriptionRow');
            const descValue = document.getElementById('modalDescription');
            if (state.Description.trim()) {
                descRow.classList.remove('hidden');
                descValue.textContent = state.Description;
            } else {
                descRow.classList.add('hidden');
            }
        }

        // ===== Validate Form =====
        function isFormValid() {
            return state.amount && parseFloat(state.amount) > 0 &&
                state.accountname && state.accountnumber && state.bankname && state.pin;
        }

        // ===== Update Button State =====
        function updateButtonState() {
            previewBtn.disabled = !isFormValid();
        }

        // ===== Input Event Handlers =====
        function setupInputListeners() {
            // Amount input
            amountInput?.addEventListener('input', function () {
                state.amount = this.value;
                // Validate max balance
                if (parseFloat(state.amount) > state.availableBalance) {
                    state.amount = state.availableBalance.toString();
                    this.value = state.amount;
                }
                updateSummary();
                updateButtonState();
            });

            // Quick amount buttons
            document.querySelectorAll('.quick-amount-btn').forEach(btn => {
                btn.addEventListener('click', function () {
                    const amount = this.getAttribute('data-amount');
                    if (amount === 'all') {
                        state.amount = state.availableBalance.toString();
                    } else {
                        state.amount = amount;
                    }
                    amountInput.value = state.amount;
                    updateSummary();
                    updateButtonState();
                });
            });

            // Other inputs
            accountnameInput?.addEventListener('input', (e) => { state.accountname = e.target.value; updateButtonState(); });
            accountnumberInput?.addEventListener('input', (e) => { state.accountnumber = e.target.value; updateButtonState(); });
            banknameInput?.addEventListener('input', (e) => { state.bankname = e.target.value; updateButtonState(); });
            accounttypeSelect?.addEventListener('change', (e) => { state.Accounttype = e.target.value; });
            descriptionInput?.addEventListener('input', (e) => { state.Description = e.target.value; updateSummary(); });
            pinInput?.addEventListener('input', (e) => { state.pin = e.target.value; updateButtonState(); });
        }

        // ===== PIN Toggle =====
        document.getElementById('pinToggle')?.addEventListener('click', function () {
            const isPassword = pinInput.type === 'password';
            pinInput.type = isPassword ? 'text' : 'password';
            document.getElementById('pinToggleIcon').setAttribute('data-lucide', isPassword ? 'eye-off' : 'eye');
            if (typeof lucide !== 'undefined') lucide.createIcons();
        });

        // ===== Preview Button =====
        document.getElementById('transferForm')?.addEventListener('submit', function (e) {
            e.preventDefault();
            if (!isFormValid()) return;

            updateSummary();
            previewModal.show();
        });

        // ===== Confirm Transfer =====
        confirmTransferBtn?.addEventListener('click', function () {
            if (state.isSubmitting) return;

            // Validate PIN length (example: 4-6 digits)
            if (!/^\d{4,6}$/.test(state.pin)) {
                showToast('Please enter a valid 4-6 digit PIN', 'error');
                return;
            }

            // Show loading state
            state.isSubmitting = true;
            confirmBtnContent.classList.add('d-none');
            confirmBtnSpinner.classList.remove('d-none');
            confirmBtnText.textContent = 'Processing...';
            confirmTransferBtn.disabled = true;

            // Simulate API call (replace with actual fetch)
            setTimeout(() => {
                showToast('✓ Transfer submitted successfully! Reference: TXN-' + Date.now().toString().slice(-6), 'success');

                // Reset form
                document.getElementById('transferForm').reset();
                state.amount = state.accountname = state.accountnumber = state.bankname = state.Description = state.pin = '';
                state.Accounttype = 'Online Banking';
                summaryCard.classList.add('hidden');
                updateButtonState();

                // Close modal
                previewModal.hide();

                // Restore button
                state.isSubmitting = false;
                confirmBtnContent.classList.remove('d-none');
                confirmBtnSpinner.classList.add('d-none');
                confirmBtnText.textContent = 'Confirm Transfer';
                confirmTransferBtn.disabled = false;

                if (typeof lucide !== 'undefined') lucide.createIcons();

                // In production, submit form:
                // document.getElementById('transferForm').submit();
            }, 2500);
        });

        // ===== Input Focus Effects =====
        document.querySelectorAll('.form-control-custom, .form-select-custom').forEach(input => {
            input.addEventListener('focus', function () {
                this.closest('.input-wrapper')?.querySelector('.input-icon')?.style.setProperty('color', 'var(--primary-color)');
            });
            input.addEventListener('blur', function () {
                this.closest('.input-wrapper')?.querySelector('.input-icon')?.style.setProperty('color', '#9ca3af');
            });
        });

        // ===== Initialize =====
        setupInputListeners();
        updateSummary();
        updateButtonState();

        // Set available balance from backend (example)
        state.availableBalance = 0; // Replace with {{ user.balance|floatformat:2 }}
        document.getElementById('availableBalance').textContent = formatCurrency(state.availableBalance);
    });
})();