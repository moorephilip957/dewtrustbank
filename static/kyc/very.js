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

            section.classList.add('animate');

            observer.observe(section);
        });

        // First section visible immediately
        const firstSection = document.querySelector('.form-section');

        if (firstSection) {
            firstSection.classList.add('visible');
        }

        // Document type selection
        document.querySelectorAll('.doc-type-card').forEach(card => {

            card.addEventListener('click', function () {

                document.querySelectorAll('.doc-type-card').forEach(c => {
                    c.classList.remove('active');
                });

                this.classList.add('active');

                const radio = this.querySelector('input[type="radio"]');

                if (radio) {
                    radio.checked = true;
                }
            });
        });

        // File upload functionality
        function setupFileUpload(
            uploadAreaId,
            fileInputId,
            previewContainerId,
            previewImgId,
            fileNameId,
            removeBtnId,
            uploadPromptId
        ) {

            const uploadArea = document.getElementById(uploadAreaId);
            const fileInput = document.getElementById(fileInputId);
            const previewContainer = document.getElementById(previewContainerId);
            const previewImg = document.getElementById(previewImgId);
            const fileName = document.getElementById(fileNameId);
            const removeBtn = document.getElementById(removeBtnId);
            const uploadPrompt = document.getElementById(uploadPromptId);

            if (
                !uploadArea ||
                !fileInput ||
                !previewContainer ||
                !previewImg ||
                !fileName ||
                !removeBtn ||
                !uploadPrompt
            ) {
                return;
            }

            // Click upload area
            uploadArea.addEventListener('click', function (e) {

                if (
                    e.target.closest('.upload-preview') ||
                    e.target.closest('.btn-remove')
                ) {
                    return;
                }

                fileInput.click();
            });

            // File selected
            fileInput.addEventListener('change', function () {

                if (this.files && this.files[0]) {

                    const file = this.files[0];

                    // Validate file size
                    if (file.size > 2 * 1024 * 1024) {

                        alert('File size exceeds 2MB.');

                        this.value = '';

                        return;
                    }

                    // Show file name
                    fileName.textContent =
                        file.name.length > 30
                            ? file.name.substring(0, 27) + '...'
                            : file.name;

                    // Preview image
                    if (file.type.match('image.*')) {

                        const reader = new FileReader();

                        reader.onload = function (e) {

                            previewImg.src = e.target.result;

                            uploadPrompt.classList.add('d-none');

                            previewContainer.classList.remove('d-none');

                            previewContainer.style.display = 'block';
                        };

                        reader.readAsDataURL(file);
                    }
                }
            });

            // Remove file
            removeBtn.addEventListener('click', function (e) {

                e.preventDefault();

                e.stopPropagation();

                fileInput.value = '';

                previewImg.src = '';

                fileName.textContent = '';

                uploadPrompt.classList.remove('d-none');

                previewContainer.classList.add('d-none');

                previewContainer.style.display = 'none';
            });

            // Prevent browser default drag events
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {

                uploadArea.addEventListener(eventName, function (e) {

                    e.preventDefault();

                    e.stopPropagation();

                }, false);
            });

            // Add drag style
            ['dragenter', 'dragover'].forEach(eventName => {

                uploadArea.addEventListener(eventName, function () {

                    uploadArea.classList.add('drag-over');

                }, false);
            });

            // Remove drag style
            ['dragleave', 'drop'].forEach(eventName => {

                uploadArea.addEventListener(eventName, function () {

                    uploadArea.classList.remove('drag-over');

                }, false);
            });

            // Handle dropped files
            uploadArea.addEventListener('drop', function (e) {

                const dt = e.dataTransfer;

                const files = dt.files;

                if (files.length) {

                    fileInput.files = files;

                    const event = new Event('change', { bubbles: true });

                    fileInput.dispatchEvent(event);
                }

            }, false);
        }

        // Front upload
        setupFileUpload(
            'frontUploadArea',
            'frontimg',
            'frontPreview',
            'frontPreviewImg',
            'frontFileName',
            'frontRemove',
            'frontUploadPrompt'
        );

        // Back upload
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

        // Input validation UI only
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