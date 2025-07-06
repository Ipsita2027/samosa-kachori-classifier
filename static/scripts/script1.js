document.addEventListener('DOMContentLoaded', () => {
// Get references to the file input and the image preview elements
const imageFileInput = document.getElementById('imageFile');
const imagePreview = document.getElementById('imagePreview');
const previewText = document.getElementById('previewText');
const previewText2 = document.getElementById('previewText2');
const previewText3 = document.getElementById('previewText3');

// Add an event listener to the file input for when its value changes
imageFileInput.addEventListener('change', (event) => {
    const file = event.target.files[0]; // Get the first selected file

    if (file) {
        // Create a FileReader object to read the file content
        const reader = new FileReader();

        // Set the onload event handler for the FileReader
        reader.onload = (e) => {
            // When the file is loaded, set the src of the image preview
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block'; // Make the image visible
            previewText.style.display = 'none';
            previewText2.style.display = 'none';
            previewText3.style.display = 'none'; // Hide the "No image selected" text
        };

        // Read the file as a Data URL (base64 encoded string)
        reader.readAsDataURL(file);
    } else {
        // If no file is selected, reset the image preview
        imagePreview.src = '#';
        imagePreview.style.display = 'none'; // Hide the image
        previewText.style.display = 'block'; // Show the "No image selected" text
        previewText2.style.display = 'block';
        previewText3.style.display = 'block';
    
    }
});
});