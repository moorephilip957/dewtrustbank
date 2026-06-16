(() => {
    document.addEventListener('DOMContentLoaded', function () {

        if (typeof lucide !== 'undefined') lucide.createIcons();

        // =========================
        // SUMMARY UPDATE (NO STATE)
        // =========================
        function updateSummary() {
            const amount = parseFloat(document.getElementById('id_amount').value || 0);
            const name = document.getElementById('id_beneficiary_name').value;
            const number = document.getElementById('id_beneficiary_number').value;
            const bank = document.getElementById('id_bank_name').value;
            const type = document.getElementById('id_transfer_type').value;
            const desc = document.getElementById('id_description').value;

            const total = amount;

            document.getElementById('summaryAmount').textContent = amount.toFixed(2);
            document.getElementById('summaryTotal').textContent = total.toFixed(2);

            document.getElementById('modalAmount').textContent = amount.toFixed(2);
            document.getElementById('modalTotal').textContent = total.toFixed(2);

            document.getElementById('modalRecipient').textContent = name || '-';
            document.getElementById('modalAccountNumber').textContent = number || '-';
            document.getElementById('modalBank').textContent = bank || '-';
            document.getElementById('modalAccountType').textContent = type || '-';

            const descRow = document.getElementById('modalDescriptionRow');
            const descValue = document.getElementById('modalDescription');

            if (desc && desc.trim()) {
                descRow.classList.remove('hidden');
                descValue.textContent = desc;
            } else {
                descRow.classList.add('hidden');
            }

            const summaryCard = document.getElementById('summaryCard');
            if (amount > 0) summaryCard.classList.remove('hidden');
            else summaryCard.classList.add('hidden');
        }

        // =========================
        // FORM VALIDATION (UI ONLY)
        // =========================
        function isFormValid() {
            const amount = parseFloat(document.getElementById('id_amount').value || 0);
            const name = document.getElementById('id_beneficiary_name').value;
            const number = document.getElementById('id_beneficiary_number').value;
            const bank = document.getElementById('id_bank_name').value;
            const pin = document.getElementById('id_transfer_pin').value;

            return amount > 0 && name && number && bank && pin;
        }

        function updateButtonState() {
            document.getElementById('previewBtn').disabled = !isFormValid();
        }

        // =========================
        // INPUT LISTENERS
        // =========================
        function bindInputs() {
            const fields = [
                'id_amount',
                'id_beneficiary_name',
                'id_beneficiary_number',
                'id_bank_name',
                'id_transfer_type',
                'id_description',
                'id_transfer_pin'
            ];

            fields.forEach(id => {
                document.getElementById(id)?.addEventListener('input', () => {
                    updateSummary();
                    updateButtonState();
                });
            });
        }

        // =========================
        // PIN TOGGLE
        // =========================
        document.getElementById('pinToggle')?.addEventListener('click', function () {
            const pin = document.getElementById('id_transfer_pin');
            const icon = document.getElementById('pinToggleIcon');

            const hidden = pin.type === 'password';
            pin.type = hidden ? 'text' : 'password';

            icon.setAttribute('data-lucide', hidden ? 'eye-off' : 'eye');
            if (typeof lucide !== 'undefined') lucide.createIcons();
        });

        // =========================
        // PREVIEW (SHOW MODAL ONLY)
        // =========================
        document.getElementById('transferForm')?.addEventListener('submit', function (e) {

            // Let HTML validation run first
            if (!this.checkValidity()) {
                this.reportValidity(); // shows native "required field" messages
                return;
            }
            e.preventDefault();

            if (!isFormValid()) return;

            updateSummary();

            const modal = new bootstrap.Modal(document.getElementById('previewModal'));
            modal.show();
        });

        // =========================
        // FINAL SUBMIT TO DJANGO
        // =========================
        document.getElementById('confirmTransferBtn')?.addEventListener('click', function () {
            const btn = this;
            const spinner = document.getElementById('confirmBtnSpinner');
            const text = document.getElementById('confirmBtnText');

            // show spinner
            spinner.classList.remove('d-none');
            btn.disabled = true;

            // optional: change text (nice UX)
            text.textContent = 'Processing...';

            // submit form
            document.getElementById('transferForm').submit();
        });

        // =========================
        // INPUT FOCUS UI EFFECT
        // =========================
        document.querySelectorAll('.form-control-custom, .form-select-custom').forEach(input => {
            input.addEventListener('focus', function () {
                this.closest('.input-wrapper')
                    ?.querySelector('.input-icon')
                    ?.style.setProperty('color', 'var(--primary-color)');
            });

            input.addEventListener('blur', function () {
                this.closest('.input-wrapper')
                    ?.querySelector('.input-icon')
                    ?.style.setProperty('color', '#9ca3af');
            });
        });

        // =========================
        // INIT
        // =========================
        bindInputs();
        updateSummary();
        updateButtonState();

    });
})();