const input = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const form = document.getElementById('uploadForm');
const errorMsg = document.getElementById('errorMsg');

// Preview image
input.addEventListener('change', function () {
    const file = this.files[0];

    if (file) {
        preview.style.display = "block";
        preview.src = URL.createObjectURL(file);
        errorMsg.textContent = ""; // clear error
    }
});

// Form validation
form.addEventListener('submit', function (e) {
    if (!input.files.length) {
        e.preventDefault();
        errorMsg.textContent = "⚠️ Please upload an image first!";
    }
});