const uploadForm = document.getElementById('uploadForm');
const imageInput = document.getElementById('imageInput');
const previewImage = document.getElementById('preview');
const outputLabel = document.getElementById('line1');


outputLabel.textContent = "Please choose an image file.";
imageInput.addEventListener('change', function () {
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();

        reader.addEventListener('load', function () {
            previewImage.src = reader.result;
        });

        reader.readAsDataURL(file);
        outputLabel.textContent = "Please click on predict to detect defect.";
    } else {
        previewImage.src = '../static/photo-icon-image.png';
        outputLabel.textContent = "Please choose an image file.";
    }
});

submitButton.addEventListener('submit', function (event) {
    outputLabel.textContent = "Please wait while the image is processing.";
})

uploadForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const section = document.getElementById('predict_result');
    section.scrollIntoView({ behavior: 'smooth' });
    
    const formData = new FormData(this);

    fetch('/upload.html', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            outputLabel.textContent = data.display_output;
            document.getElementById('predict_result').style.display = 'block';
        })
        .catch(error => {
            console.error(error);
        });
});
