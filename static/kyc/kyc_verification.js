(() => {

    document.addEventListener('DOMContentLoaded', function () {

        // Animate form sections on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.form-section').forEach(section => {
            observer.observe(section);
        });

        // Trigger initial animation for first section
        const firstSection = document.querySelector('.form-section');
        if (firstSection) firstSection.classList.add('visible');

        // Document type selection
        const docInput = document.getElementById("id_document_type");
        const docCards = document.querySelectorAll(".doc-type-card");

        docCards.forEach(card => {

            card.addEventListener("click", function () {

                // remove previous selection
                docCards.forEach(c => c.classList.remove("selected"));

                // add selected
                this.classList.add("selected");

                // set Django value
                docInput.value = this.dataset.type;

            });

        });

        // document.addEventListener("DOMContentLoaded", () => {

        //     const current = docInput.value;

        //     docCards.forEach(card => {
        //         if (card.dataset.type === current) {
        //             card.classList.add("selected");
        //         }
        //     });

        // });

        // ✅ FIXED: File upload functionality with proper preview handling
        function setupFileUpload(uploadAreaId, fileInputId, previewContainerId, previewImgId, fileNameId, removeBtnId, uploadPromptId) {
            const uploadArea = document.getElementById(uploadAreaId);
            const fileInput = document.getElementById(fileInputId);
            const previewContainer = document.getElementById(previewContainerId);
            const previewImg = document.getElementById(previewImgId);
            const fileName = document.getElementById(fileNameId);
            const removeBtn = document.getElementById(removeBtnId);
            const uploadPrompt = document.getElementById(uploadPromptId); // The label containing upload instructions

            if (!uploadArea || !fileInput || !previewContainer || !previewImg || !fileName || !removeBtn || !uploadPrompt) {
                console.warn(`Missing elements for ${uploadAreaId}. Check IDs:`);
                console.log({ uploadAreaId, fileInputId, previewContainerId, previewImgId, fileNameId, removeBtnId, uploadPromptId });
                return;
            }

            // Handle click on upload area (only trigger file input if not clicking preview/remove)
            uploadArea.addEventListener('click', function (e) {
                if (e.target.closest('.upload-preview') || e.target.closest('.btn-remove')) {
                    return;
                }
                fileInput.click();
            });

            // Handle file selection
            fileInput.addEventListener('change', function () {
                if (this.files && this.files[0]) {
                    const file = this.files[0];

                    // Validate file size (15MB max)
                    if (file.size > 15 * 1024 * 1024) {
                        alert('⚠️ File size exceeds 15MB limit. Please choose a smaller file.');
                        this.value = '';
                        return;
                    }

                    // Display file name
                    fileName.textContent = file.name.length > 30 ? file.name.substring(0, 27) + '...' : file.name;

                    // Check if file is an image
                    if (file.type.match('image.*')) {
                        const reader = new FileReader();

                        reader.onload = function (e) {
                            previewImg.src = e.target.result;
                            // ✅ FIX: Hide upload prompt, show preview container (not the whole area)
                            uploadPrompt.classList.add('d-none');
                            previewContainer.classList.remove('d-none');
                            previewContainer.style.display = 'block';
                        };

                        reader.readAsDataURL(file);
                    } else {
                        // For non-image files, just show filename
                        uploadPrompt.classList.add('d-none');
                        previewContainer.classList.remove('d-none');
                        previewContainer.style.display = 'block';
                    }
                }
            });

            // Handle file removal
            removeBtn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();

                // Reset file input
                fileInput.value = '';

                // Reset preview
                previewImg.src = '';
                fileName.textContent = '';
                // ✅ FIX: Show upload prompt, hide preview container
                uploadPrompt.classList.remove('d-none');
                previewContainer.classList.add('d-none');
                previewContainer.style.display = 'none';
            });

            // Handle drag and drop visual feedback
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                }, false);
            });

            ['dragenter', 'dragover'].forEach(eventName => {
                uploadArea.addEventListener(eventName, function () {
                    uploadArea.classList.add('drag-over');
                }, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, function () {
                    uploadArea.classList.remove('drag-over');
                }, false);
            });

            uploadArea.addEventListener('drop', function (e) {
                const dt = e.dataTransfer;
                const files = dt.files;

                if (files.length) {
                    fileInput.files = files;
                    // Trigger change event manually
                    const event = new Event('change', { bubbles: true });
                    fileInput.dispatchEvent(event);
                }
            }, false);
        }

        // ✅ Initialize all file uploads with CORRECT IDs matching HTML structure
        // Front image upload
        setupFileUpload(
            'frontUploadArea',      // uploadAreaId
            'frontimg',             // fileInputId
            'frontPreview',         // previewContainerId (the .upload-preview div)
            'frontPreviewImg',      // previewImgId (the <img> inside preview)
            'frontFileName',        // fileNameId
            'frontRemove',          // removeBtnId
            'frontUploadPrompt'     // uploadPromptId (the <label> with upload instructions) ⭐ NEW
        );

        // Back image upload
        setupFileUpload(
            'backUploadArea',
            'backimg',
            'backPreview',
            'backPreviewImg',
            'backFileName',
            'backRemove',
            'backUploadPrompt'
        );

        // Photo upload
        setupFileUpload(
            'photoUploadArea',
            'photo',
            'photoPreview',
            'photoPreviewImg',
            'photoFileName',
            'photoRemove',
            'photoUploadPrompt'
        );

        // Add input validation feedback on blur
        document.querySelectorAll('.form-control, .form-select').forEach(input => {
            input.addEventListener('blur', function () {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                }
            });

            input.addEventListener('input', function () {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    });
})();