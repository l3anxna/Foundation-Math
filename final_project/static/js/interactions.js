document.getElementById('file').addEventListener('change', function(e) {
    const reader = new FileReader();
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    
    reader.onload = function() {
        imagePreview.src = reader.result;
        previewContainer.classList.remove('hidden');
        previewContainer.classList.add('fade-in');
    }
    
    if (e.target.files[0]) {
        reader.readAsDataURL(e.target.files[0]);
    }
});

document.querySelectorAll('.filter-option').forEach(option => {
    option.addEventListener('click', function() {
        document.querySelectorAll('.filter-option').forEach(opt => {
            opt.classList.remove('selected');
        });
        this.classList.add('selected');
    });
});

document.querySelector('form').addEventListener('submit', function() {
    const submitButton = this.querySelector('button[type="submit"]');
    submitButton.innerHTML = 'Processing... <div class="spinner"></div>';
    submitButton.setAttribute('disabled', true);
});

function adjustImageSizes() {
    document.querySelectorAll('.image-box img').forEach(img => {
        const container = img.closest('.image-box');
        img.style.maxHeight = `${container.clientHeight * 0.8}px`;
    });
}

window.addEventListener('resize', adjustImageSizes);