(() => {
    document.addEventListener('DOMContentLoaded', function () {

        if (typeof lucide !== 'undefined') lucide.createIcons();

        const loanInfoSection = document.getElementById('loanInfoSection');
        const loanFormSection = document.getElementById('loanFormSection');

        const applyNowBtn = document.getElementById('applyNowBtn');
        const backToInfoBtn = document.getElementById('backToInfoBtn');
        const backToInfoBtn2 = document.getElementById('backToInfoBtn2');
        const cancelBtn = document.getElementById('cancelBtn');

        function showForm() {
            loanInfoSection.classList.add('d-none');
            loanFormSection.classList.remove('d-none');

            if (typeof lucide !== 'undefined') lucide.createIcons();
        }

        function showInfo() {
            loanFormSection.classList.add('d-none');
            loanInfoSection.classList.remove('d-none');

            if (typeof lucide !== 'undefined') lucide.createIcons();
        }

        applyNowBtn?.addEventListener('click', showForm);
        backToInfoBtn?.addEventListener('click', showInfo);
        backToInfoBtn2?.addEventListener('click', showInfo);
        cancelBtn?.addEventListener('click', showInfo);

    });

})();