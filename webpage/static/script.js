document.addEventListener("DOMContentLoaded", () => {
    const icons = document.querySelectorAll(".icon");

    // Function to clear all highlights
    function clearHighlights() {
        icons.forEach(icon => icon.classList.remove("highlighted"));
    }

    // Highlight the matching icon if emotion exists
    if (detectedEmotion) {
        clearHighlights();
        icons.forEach(icon => {
            if (icon.dataset.emotion === detectedEmotion) {
                icon.classList.add("highlighted");
            }
        });
    }
});

