// Initialize Lucide Icons (if using alongside Bootstrap Icons)
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}

// Page Loader
window.addEventListener('load', function () {
    setTimeout(function () {
        document.getElementById('pageLoader').classList.add('hidden');
    }, 800);
});

// Time & Greeting Updates
function updateDateTime() {
    const now = new Date();

    // Time
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    const currentTime = document.getElementById('currentTime');
    if (currentTime) {
        currentTime.textContent = `${hours}:${minutes}:${seconds}`;
    }

    // Greeting
    const hour = now.getHours();
    let greeting = 'Good Evening';

    if (hour < 12) greeting = 'Good Morning';
    else if (hour < 18) greeting = 'Good Afternoon';

    const greetingEl = document.getElementById('greeting');
    if (greetingEl) {
        greetingEl.textContent = greeting;
    }

    // Date
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };

    const dateString = now.toLocaleDateString(undefined, options);

    const currentDate = document.getElementById('currentDate');
    if (currentDate) {
        currentDate.textContent = dateString;
    }

    const headerDate = document.getElementById('headerDate');
    if (headerDate) {
        headerDate.textContent = dateString;
    }
}

updateDateTime();
setInterval(updateDateTime, 1000);

// Balance Toggle
let balanceVisible = true;

const toggleBtn = document.getElementById('toggleBalance');

if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
        balanceVisible = !balanceVisible;

        const display = document.getElementById('balanceDisplay');
        const hidden = document.getElementById('balanceHidden');
        const icon = document.getElementById('balanceIcon');

        if (balanceVisible) {
            display?.classList.remove('d-none');
            hidden?.classList.add('d-none');
            if (icon) icon.className = 'bi bi-eye-slash';
        } else {
            display?.classList.add('d-none');
            hidden?.classList.remove('d-none');
            if (icon) icon.className = 'bi bi-eye';
        }
    });
}

// Mobile Menu Toggle
const mobileMenuModal = document.getElementById('mobileMenuModal');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const openMobileMenu = document.getElementById('openMobileMenu');
const closeMobileMenu = document.getElementById('closeMobileMenu');

function openMobileMenuModal() {
    mobileMenuModal.classList.remove('hide');
    mobileMenuModal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeMobileMenuModal() {
    mobileMenuModal.classList.remove('show');
    mobileMenuModal.classList.add('hide');
    setTimeout(() => {
        mobileMenuModal.classList.remove('hide');
        document.body.style.overflow = '';
    }, 200);
}

openMobileMenu?.addEventListener('click', openMobileMenuModal);
mobileMenuToggle?.addEventListener('click', openMobileMenuModal);
closeMobileMenu?.addEventListener('click', closeMobileMenuModal);
mobileMenuModal?.addEventListener('click', function (e) {
    if (e.target === mobileMenuModal) closeMobileMenuModal();
});

// Copy to Clipboard
function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        btn.classList.add('copied');
        const icon = btn.querySelector('i');
        icon.className = 'bi bi-check-lg';
        setTimeout(() => {
            btn.classList.remove('copied');
            icon.className = 'bi bi-clipboard';
        }, 2000);
    });
}

// Close dropdowns when clicking outside (Bootstrap handles most, but extra safety)
document.addEventListener('click', function (e) {
    if (!e.target.closest('.dropdown')) {
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        dropdowns.forEach(dropdown => {
            const bsDropdown = bootstrap.Dropdown.getInstance(dropdown.parentElement.querySelector('[data-bs-toggle="dropdown"]'));
            if (bsDropdown) bsDropdown.hide();
        });
    }
});

// Responsive sidebar toggle for tablet (optional enhancement)
function checkScreenSize() {
    const sidebar = document.getElementById('desktopSidebar');
    const mainContent = document.querySelector('.main-content');
    if (window.innerWidth < 769) {
        sidebar?.classList.remove('show');
        mainContent?.classList.remove('sidebar-open');
    }
}
window.addEventListener('resize', checkScreenSize);
checkScreenSize();