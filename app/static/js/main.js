/**
 * Main JavaScript for AI Resume Analyzer
 */

document.addEventListener('DOMContentLoaded', function() {
    // File upload handling
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('resume-upload');
    
    if (uploadArea && fileInput) {
        // Click on upload area to trigger file input, but only if the click wasn't on the input itself
        uploadArea.addEventListener('click', (e) => {
            // Don't trigger another click if the user clicked on the file input directly
            if (e.target !== fileInput && !e.target.contains(fileInput)) {
                fileInput.click();
            }
        });
        
        // Drag and drop functionality
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('border-primary');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('border-primary');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-primary');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileName(e.dataTransfer.files[0]?.name);
            }
        });
        
        // Update file name display when a file is selected
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                updateFileName(e.target.files[0].name);
            }
        });
    }
    
    // Function to update the displayed file name
    function updateFileName(fileName) {
        const fileNameDisplay = document.getElementById('file-name');
        if (fileNameDisplay) {
            fileNameDisplay.textContent = 'Selected file: ' + fileName;
            fileNameDisplay.classList.add('text-success');
        }
    }
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-dismissible)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
    
    // Print functionality for results page
    const printButton = document.querySelector('.btn-print');
    if (printButton) {
        printButton.addEventListener('click', () => {
            window.print();
        });
    }
    
    // Expand all accordion items for printing
    window.addEventListener('beforeprint', () => {
        const accordionItems = document.querySelectorAll('.accordion-collapse');
        accordionItems.forEach(item => {
            item.classList.add('show');
        });
    });
    
    // Animation for score counters on results page
    const scoreElements = document.querySelectorAll('.animate-score');
    if (scoreElements.length) {
        scoreElements.forEach(element => {
            const targetScore = parseInt(element.textContent);
            animateCounter(element, 0, targetScore, 1500);
        });
    }
    
    // Animate counter from start to end value
    function animateCounter(element, start, end, duration) {
        const range = end - start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / range));
        
        let current = start;
        const timer = setInterval(() => {
            current += increment;
            element.textContent = current;
            
            if (current === end) {
                clearInterval(timer);
            }
        }, stepTime);
    }
});