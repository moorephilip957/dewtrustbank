(() => {

    document.addEventListener('DOMContentLoaded', function () {
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') lucide.createIcons();


        // ===== Form Elements =====
        const supportForm = document.getElementById('supportTicketForm');
        const submitBtn = document.getElementById('submitBtn');
        const submitSpinner = document.getElementById('submitSpinner');
        const submitText = document.getElementById('submitText');
        const clearBtn = document.getElementById('clearBtn');
        const messageTextarea = document.getElementById('message');

        // ===== Auto-resize Textarea =====
        function autoResize(el) {
            el.style.height = 'auto';
            el.style.height = Math.min(el.scrollHeight, 300) + 'px';
        }

        messageTextarea?.addEventListener('input', function () {
            autoResize(this);
        });

        // Initialize textarea height on load
        if (messageTextarea && messageTextarea.value) {
            autoResize(messageTextarea);
        }

        // ===== Clear Form Handler =====
        clearBtn?.addEventListener('click', function () {
            supportForm.reset();
            if (messageTextarea) {
                messageTextarea.style.height = 'auto';
            }
            showToast('Form cleared', 'info', 2000);
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
    });

})();