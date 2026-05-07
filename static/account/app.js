// ===== Helpers =====
const $ = (id) => document.getElementById(id);

// ===== Page Loader =====
window.addEventListener('load', () => {
    const loader = $('pageLoader');
    setTimeout(() => {
        loader.classList.add('hidden');
        setTimeout(() => loader.remove(), 400);
    }, 700);
});

// ===== Password Toggle =====
function initPasswordToggle(toggleId, inputId, iconId) {
    const toggleBtn = $(toggleId);
    const input = $(inputId);
    const icon = $(iconId);

    if (!toggleBtn || !input || !icon) return;

    toggleBtn.addEventListener('click', () => {
        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        icon.className = isPassword ? 'bi bi-eye-slash' : 'bi bi-eye';
        toggleBtn.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
    });
}

// Initialize password toggle (ONLY ONCE)
initPasswordToggle('togglePassword', 'password', 'eyeIcon');

// ===== Form Submission (Login Demo) =====
$('loginForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = $('username').value;

    alert(`Demo mode: Would sign in as "${username}"\n\n🔐 In production:\n• Submit to HTTPS endpoint\n• Use CSRF tokens\n• Validate server-side`);

    e.target.reset();
});

// ===== Multi-Step Form Logic =====
const steps = ['step1', 'step2', 'step3', 'step4'];
let currentStep = 1;
const totalSteps = steps.length;

const prevBtn = $('prevBtn');
const nextBtn = $('nextBtn');
const submitBtn = $('submitBtn');
const progressBar = $('progressBar');
const currentStepEl = $('currentStep');

function updateStep() {
    // Toggle steps
    steps.forEach((id, idx) => {
        $(id).classList.toggle('active', idx + 1 === currentStep);
    });

    // Progress bar
    const progress = (currentStep / totalSteps) * 100;
    progressBar.style.width = `${progress}%`;
    currentStepEl.textContent = currentStep;

    // Indicators
    for (let i = 1; i <= totalSteps; i++) {
        const indicator = $(`stepIndicator${i}`);
        const label = $(`label${i}`);

        indicator.classList.remove('active', 'completed');
        label.classList.remove('active');

        if (i < currentStep) indicator.classList.add('completed');
        if (i === currentStep) {
            indicator.classList.add('active');
            label.classList.add('active');
        }
    }

    // Buttons
    prevBtn.style.display = currentStep === 1 ? 'none' : 'inline-flex';
    nextBtn.style.display = currentStep === totalSteps ? 'none' : 'inline-flex';
    submitBtn.style.display = currentStep === totalSteps ? 'inline-flex' : 'none';
}

prevBtn?.addEventListener('click', () => {
    if (currentStep > 1) {
        currentStep--;
        updateStep();
    }
});

nextBtn?.addEventListener('click', () => {
    if (validateStep(currentStep) && currentStep < totalSteps) {
        currentStep++;
        updateStep();
    }
});

function validateStep(step) {
    const stepEl = $(`step${step}`);
    const required = stepEl.querySelectorAll('[required]');
    let valid = true;

    required.forEach(input => {
        const isValid = input.value.trim();
        input.classList.toggle('is-invalid', !isValid);
        if (!isValid) valid = false;
    });

    // Password match (step 4)
    if (step === 4) {
        const pwd = document.querySelector('[name="password"]').value;
        const confirm = document.querySelector('[name="id_password2"]').value;
        const error = $('passwordMatchError');

        const match = pwd && confirm && pwd === confirm;
        error.classList.toggle('d-none', match);

        if (!match) valid = false;
    }

    return valid;
}

// ===== accouint_type Selection =====
document.querySelectorAll('.account-type-card').forEach(card => {
    card.addEventListener('click', function () {

        // remove previous selection
        document.querySelectorAll('.account-type-card')
            .forEach(c => c.classList.remove('selected'));

        // select current card
        this.classList.add('selected');

        // get account type ID
        const value = this.dataset.value;

        // update Django hidden select field
        const field = document.querySelector('[name="account_type"]');

        if (field) {
            field.value = value;

            // important for Django validation/UX
            field.dispatchEvent(new Event('change'));
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const first = document.querySelector('.account-type-card');
    if (first) first.click();
});

// ===== Password Strength Meter =====
const strengthContainer = $('strengthContainer');
const strengthFill = $('strengthFill');
const strengthLabel = $('strengthLabel');

const rules = {
    length: $('ruleLength'),
    upper: $('ruleUpper'),
    number: $('ruleNumber'),
    special: $('ruleSpecial')
};

$('password')?.addEventListener('input', function () {
    const pwd = this.value;

    if (!pwd) {
        strengthContainer.style.display = 'none';
        return;
    }

    strengthContainer.style.display = 'block';

    const checks = {
        length: pwd.length >= 8,
        upper: /[A-Z]/.test(pwd),
        number: /[0-9]/.test(pwd),
        special: /[^A-Za-z0-9]/.test(pwd)
    };

    // Rule UI update
    Object.entries(rules).forEach(([key, el]) => {
        const icon = el.querySelector('i');
        const passed = checks[key];

        icon.className = passed
            ? 'bi bi-check-circle-fill text-success small me-1'
            : 'bi bi-circle small me-1';

        el.classList.toggle('text-success', passed);
    });

    // Strength score
    const score = Object.values(checks).filter(Boolean).length;

    const config = [
        { max: 1, width: 20, label: 'Very Weak', className: 'strength-weak' },
        { max: 2, width: 40, label: 'Weak', className: 'strength-weak' },
        { max: 3, width: 70, label: 'Good', className: 'strength-fair' },
        { max: 4, width: 100, label: 'Strong', className: 'strength-strong' }
    ].find(c => score <= c.max);

    strengthFill.style.width = `${config.width}%`;
    strengthFill.className = `strength-fill ${config.className}`;

    strengthLabel.textContent = config.label;
    strengthLabel.className = `fw-medium ${
        score <= 2 ? 'text-danger' :
        score === 3 ? 'text-warning' :
        'text-success'
    }`;
});

// ===== Init =====
updateStep();