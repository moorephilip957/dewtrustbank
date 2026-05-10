(() => {

    function copyWallet() {

        let copyText =
            document.getElementById("walletInput");

        copyText.select();

        copyText.setSelectionRange(0, 99999);

        navigator.clipboard.writeText(copyText.value);

    }

    /* FILE */

    const uploadBox =
        document.getElementById("uploadBox");

    const fileInput =
        document.getElementById("fileInput");

    uploadBox.addEventListener("click", () => {

        fileInput.click();

    });

    uploadBox.addEventListener("dragover", (e) => {

        e.preventDefault();

        uploadBox.style.borderColor = "#0147E1";
        uploadBox.style.background = "#f5f9ff";

    });

    uploadBox.addEventListener("dragleave", () => {

        uploadBox.style.borderColor = "#cfd7e6";
        uploadBox.style.background = "#fff";

    });

    uploadBox.addEventListener("drop", (e) => {

        e.preventDefault();

        uploadBox.style.borderColor = "#cfd7e6";
        uploadBox.style.background = "#fff";

        if (e.dataTransfer.files.length) {

            fileInput.files = e.dataTransfer.files;

            showPreview(
                e.dataTransfer.files[0]
            );

        }

    });

    fileInput.addEventListener("change", function () {

        if (this.files.length) {

            showPreview(this.files[0]);

        }

    });

    function showPreview(file) {

        document.getElementById(
            "uploadDefault"
        ).style.display = "none";

        document.getElementById(
            "previewContainer"
        ).style.display = "block";

        document.getElementById(
            "fileName"
        ).innerText = file.name;

        const previewImage =
            document.getElementById(
                "previewImage"
            );

        if (file.type.startsWith("image/")) {

            const reader = new FileReader();

            reader.onload = function (e) {

                previewImage.src =
                    e.target.result;

            }

            reader.readAsDataURL(file);

        } else {

            previewImage.src =
                "https://cdn-icons-png.flaticon.com/512/337/337946.png";

        }

    }

    document.getElementById("removeFileBtn")
        .addEventListener("click", removeFile);


    function removeFile() {
        const uploadError = document.getElementById("uploadError");


        fileInput.value = "";

        updateState();

        uploadError.classList.remove("d-none");
        uploadError.textContent = "Please upload a proof of payment";

        document.getElementById(
            "uploadDefault"
        ).style.display = "block";

        document.getElementById(
            "previewContainer"
        ).style.display = "none";

    }

    const submitBtn = document.getElementById("submitBtn");
    const uploadError = document.getElementById("uploadError");

    if (!fileInput || !submitBtn) return;

    function updateState() {

        if (fileInput.files && fileInput.files.length > 0) {

            submitBtn.disabled = false;
            uploadError.classList.add("d-none");

        } else {

            submitBtn.disabled = true;

        }
    }

    // initial state
    updateState();

    fileInput.addEventListener("change", updateState);
})();
