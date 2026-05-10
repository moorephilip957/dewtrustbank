(() => {

    document.addEventListener('DOMContentLoaded', () => {

        // Initialize Lucide Icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        const installBtn = document.getElementById('main-install-button');
        const showInstructionsBtn = document.getElementById('show-instructions');
        const hideInstructionsBtn = document.getElementById('hide-instructions');
        const manualInstructions = document.getElementById('manual-instructions');

        let deferredPrompt = null;

        // Capture PWA install event
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
        });

        // Main install button
        installBtn?.addEventListener('click', async () => {

            // Supported browsers
            if (deferredPrompt) {
                deferredPrompt.prompt();

                try {
                    await deferredPrompt.userChoice;
                } catch (err) {
                    console.log(err);
                }

                deferredPrompt = null;
                return;
            }

            // iOS devices
            const ua = navigator.userAgent.toLowerCase();

            if (/iphone|ipad|ipod/.test(ua)) {
                const iosModal = new bootstrap.Modal(
                    document.getElementById('iosInstallModal')
                );

                iosModal.show();
                return;
            }

            // Fallback manual instructions
            manualInstructions?.classList.remove('d-none');

            manualInstructions?.scrollIntoView({
                behavior: 'smooth'
            });
        });

        // Show manual instructions
        showInstructionsBtn?.addEventListener('click', () => {
            manualInstructions?.classList.remove('d-none');

            manualInstructions?.scrollIntoView({
                behavior: 'smooth'
            });
        });

        // Hide manual instructions
        hideInstructionsBtn?.addEventListener('click', () => {
            manualInstructions?.classList.add('d-none');
        });

    });
})();