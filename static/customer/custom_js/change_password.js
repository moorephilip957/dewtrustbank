(() => {

    document.addEventListener('DOMContentLoaded', function () {
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') lucide.createIcons();

        // ===== Password Visibility Toggle =====
        document.querySelectorAll('.password-toggle').forEach(btn => {
            btn.addEventListener('click', function () {
                const targetId = this.getAttribute('data-target');
                const input = document.getElementById(targetId);
                const icon = this.querySelector('.toggle-icon');

                if (input.type === 'password') {
                    input.type = 'text';
                    icon.setAttribute('data-lucide', 'eye-off');
                } else {
                    input.type = 'password';
                    icon.setAttribute('data-lucide', 'eye');
                }
                if (typeof lucide !== 'undefined') lucide.createIcons();
            });
        });

        const password = document.getElementById('password');
        const passwordError = document.getElementById('passwordError');

        password.addEventListener('input', function () {
            password.setCustomValidity('');
            passwordError.textContent = '';

            if (!password.checkValidity()) {
                password.setCustomValidity(
                    'Password must contain uppercase, lowercase, number and be at least 8 characters.'
                );

                passwordError.textContent = password.validationMessage;
            }
        });

        // ===== Password Match Validation =====
        const newPassword = document.getElementById('password');
        const confirmPassword = document.getElementById('password_confirmation');
        const matchMsg = document.getElementById('passwordMatchMsg');
        const mismatchMsg = document.getElementById('passwordMismatchMsg');

        function checkPasswordMatch() {
            if (!newPassword.value || !confirmPassword.value) {
                matchMsg.classList.add('d-none');
                mismatchMsg.classList.add('d-none');
                return;
            }
            if (newPassword.value === confirmPassword.value) {
                matchMsg.classList.remove('d-none');
                mismatchMsg.classList.add('d-none');
            } else {
                matchMsg.classList.add('d-none');
                mismatchMsg.classList.remove('d-none');
            }
        }

        newPassword?.addEventListener('input', checkPasswordMatch);
        confirmPassword?.addEventListener('input', checkPasswordMatch);

        

        // ===== Input Focus Effects =====
        document.querySelectorAll('.form-control-custom').forEach(input => {
            input.addEventListener('focus', function () {
                this.closest('.input-wrapper')?.querySelector('.input-icon')?.style.setProperty('color', 'var(--primary-color)');
            });
            input.addEventListener('blur', function () {
                this.closest('.input-wrapper')?.querySelector('.input-icon')?.style.setProperty('color', '#9ca3af');
            });
        });
    });
})();