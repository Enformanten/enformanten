let currentSchoolIndex = 0;
const schoolList = ['school1', 'school2'];  // add more schools as needed
const iframeContainer = document.getElementById('iframe-container');

function loadIframes() {
    iframeContainer.innerHTML = '';
    const iframe = document.createElement('iframe');
    iframe.src = `./templates/${schoolList[currentSchoolIndex]}`;
    iframeContainer.appendChild(iframe);
}

function toggleArrows() {
    document.getElementById('left-arrow').style.visibility = currentSchoolIndex === 0 ? 'hidden' : 'visible';
    document.getElementById('right-arrow').style.visibility = currentSchoolIndex === schoolList.length - 1 ? 'hidden' : 'visible';
}

// Navigation logic
document.getElementById('left-arrow').addEventListener('click', function() {
    if (currentSchoolIndex > 0) {
        currentSchoolIndex--;
        loadIframes();
        toggleArrows();
    }
});

document.getElementById('right-arrow').addEventListener('click', function() {
    if (currentSchoolIndex < schoolList.length - 1) {
        currentSchoolIndex++;
        loadIframes();
        toggleArrows();
    }
});

// Initialize the view
loadIframes();
toggleArrows();
