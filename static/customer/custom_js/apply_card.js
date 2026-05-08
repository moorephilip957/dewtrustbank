(() => {
    document.addEventListener('DOMContentLoaded', function () {
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') lucide.createIcons();

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

        // ===== Card Type Selection =====
        document.querySelectorAll('.card-type-option input[type="radio"]').forEach(radio => {
            const option = radio.closest('.card-type-option');

            // Set initial selected state
            if (radio.checked) {
                option.classList.add('selected');
            }

            radio.addEventListener('change', function () {
                // Remove selected from all options
                document.querySelectorAll('.card-type-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                // Add selected to current option
                option.classList.add('selected');
            });
        });

        // ===== FAQs Accordion =====
        document.querySelectorAll('.faq-question').forEach(question => {
            question.addEventListener('click', function () {
                const item = this.parentElement;
                const isActive = item.classList.contains('active');

                // Close all items
                document.querySelectorAll('.faq-item').forEach(faq => {
                    faq.classList.remove('active');
                });

                // Toggle current item
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        });

        // ===== Input Focus Effects =====
        document.querySelectorAll('.form-control-custom, .form-select-custom').forEach(input => {
            input.addEventListener('focus', function () {
                this.closest('.input-wrapper, .select-wrapper, .currency-input-wrapper')?.querySelector('.input-icon, .select-chevron, .currency-symbol')?.style.setProperty('color', 'var(--primary-color)');
            });
            input.addEventListener('blur', function () {
                this.closest('.input-wrapper, .select-wrapper, .currency-input-wrapper')?.querySelector('.input-icon, .select-chevron, .currency-symbol')?.style.setProperty('color', '#9ca3af');
            });
        });

        // ===== Daily Limit Validation =====
        const dailyLimitInput = document.getElementById('daily_limit');
        dailyLimitInput?.addEventListener('input', function () {
            const min = parseInt(this.min) || 0;
            const max = parseInt(this.max) || Infinity;
            let value = parseInt(this.value) || 0;

            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });
})();