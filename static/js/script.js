// Campus Connect - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize sidebar toggle functionality
    initSidebar();
    
    // Initialize form validation
    initFormValidation();
    
    // Initialize flash message auto-dismiss
    initFlashMessages();
    
    // Initialize profile form validation
    initProfileFormValidation();
});

/**
 * Initialize sidebar toggle functionality for mobile screens
 */
function initSidebar() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(event) {
            if (window.innerWidth <= 768 && 
                !sidebar.contains(event.target) && 
                !sidebarToggle.contains(event.target) &&
                sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
            }
        });
    }
}

/**
 * Initialize form validation for auth forms
 */
function initFormValidation() {
    const authForms = document.querySelectorAll('.auth-form');
    
    authForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Email validation
            const emailInput = form.querySelector('input[type="email"]');
            if (emailInput && !validateEmail(emailInput.value)) {
                showInputError(emailInput, 'Please enter a valid email address');
                isValid = false;
            }
            
            // Password validation
            const passwordInput = form.querySelector('input[type="password"]');
            if (passwordInput && passwordInput.value.length < 6) {
                showInputError(passwordInput, 'Password must be at least 6 characters');
                isValid = false;
            }
            
            // Role validation for signup
            if (form.id === 'signup-form') {
                const roleInputs = form.querySelectorAll('input[name="role"]');
                let roleSelected = false;
                
                roleInputs.forEach(input => {
                    if (input.checked) roleSelected = true;
                });
                
                if (!roleSelected) {
                    const roleContainer = form.querySelector('.radio-group');
                    showInputError(roleContainer, 'Please select a role');
                    isValid = false;
                }
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
        
        // Clear error on input change
        form.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', function() {
                clearInputError(input);
            });
        });
    });
}

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} - True if valid
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Show input error message
 * @param {HTMLElement} input - Input element
 * @param {string} message - Error message
 */
function showInputError(input, message) {
    clearInputError(input);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'input-error';
    errorElement.style.color = '#F44336';
    errorElement.style.fontSize = '0.9rem';
    errorElement.style.marginTop = '0.25rem';
    errorElement.textContent = message;
    
    input.parentNode.appendChild(errorElement);
    input.style.borderColor = '#F44336';
}

/**
 * Clear input error message
 * @param {HTMLElement} input - Input element
 */
function clearInputError(input) {
    const parent = input.parentNode;
    const errorElement = parent.querySelector('.input-error');
    
    if (errorElement) {
        parent.removeChild(errorElement);
    }
    
    input.style.borderColor = '';
}

/**
 * Initialize flash message auto-dismiss
 */
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 300);
        }, 5000);
    });
}

/**
 * Handle profile picture preview
 * @param {HTMLElement} input - File input element
 * @param {string} previewId - ID of image preview element
 */
function previewProfilePicture(input, previewId) {
    const preview = document.getElementById(previewId);
    
    if (input.files && input.files[0] && preview) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

/**
 * Initialize form validation for profile setup forms
 */
function initProfileFormValidation() {
    const studentProfileForm = document.querySelector('form[action*="setup/student-profile"]');
    const campusProfileForm = document.querySelector('form[action*="setup/campus-profile"]');
    
    if (studentProfileForm) {
        studentProfileForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate graduation years
            const startYear = parseInt(document.getElementById('graduation_start').value);
            const endYear = parseInt(document.getElementById('graduation_end').value);
            
            if (endYear <= startYear) {
                showInputError(document.getElementById('graduation_end'), 'End year must be after start year');
                isValid = false;
            }
            
            // Validate required fields
            ['first_name', 'last_name', 'bio', 'location', 'course'].forEach(fieldId => {
                const input = document.getElementById(fieldId);
                if (!input.value.trim()) {
                    showInputError(input, 'This field is required');
                    isValid = false;
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    if (campusProfileForm) {
        campusProfileForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate required fields
            ['campus_name', 'about', 'established_year', 'courses_offered'].forEach(fieldId => {
                const input = document.getElementById(fieldId);
                if (!input.value.trim()) {
                    showInputError(input, 'This field is required');
                    isValid = false;
                }
            });
            
            // Validate established year
            const establishedYear = parseInt(document.getElementById('established_year').value);
            const currentYear = new Date().getFullYear();
            
            if (establishedYear > currentYear) {
                showInputError(document.getElementById('established_year'), 'Year cannot be in the future');
                isValid = false;
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
}
