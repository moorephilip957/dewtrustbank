(() => {

    document.addEventListener('DOMContentLoaded', () => {

        const toggleBtn = document.getElementById('toggleCurrentPassword');

        toggleBtn?.addEventListener('click', function () {

            const input = document.getElementById('currentPassword');
            const icon = this.querySelector('i');

            if (!input) return;

            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.replace('bi-eye', 'bi-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.replace('bi-eye-slash', 'bi-eye');
            }

        });

        // Copy to clipboard functionality
        const btn = document.getElementById('copyAccountBtn');

        btn?.addEventListener('click', async function () {

            const text = this.dataset.value;
            const icon = this.querySelector('i');

            if (!text) return;

            try {
                await navigator.clipboard.writeText(text);

                const originalClass = icon.className;

                icon.className = 'bi bi-check-lg text-success';

                setTimeout(() => {
                    icon.className = originalClass;
                }, 1500);

            } catch (err) {
                console.error('Copy failed:', err);
            }

        });


        // Profile picture preview
        document.getElementById('photoUpload').addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    const preview = document.getElementById('imagePreview');
                    const img = preview.querySelector('img');
                    img.src = event.target.result;
                    preview.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });

    });


})();


