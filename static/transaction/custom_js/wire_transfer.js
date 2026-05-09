(() => {
    document.addEventListener('DOMContentLoaded', function () {

        // Lucide Icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        // Toggle PIN
        document.getElementById('togglePin')?.addEventListener('click', function () {

            const input = document.getElementById('id_transfer_pin');
            const icon = document.getElementById('pinIcon');

            if (input.type === 'password') {
                input.type = 'text';
                icon.setAttribute('data-lucide', 'eye-off');
            } else {
                input.type = 'password';
                icon.setAttribute('data-lucide', 'eye');
            }

            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        });

    });
})();