let form = document.querySelector(".login_form");
let error_paragraph = document.querySelector(".error");

// Select the password field and eye icon
const passwordField = document.getElementById('passwordField');
const togglePassword = document.getElementById('togglePassword');
const passwordIcon = document.getElementById('passwordIcon');

// Initially hide the eye icon
togglePassword.style.display = 'none';

// Show/hide the eye icon based on password input
passwordField.addEventListener('input', function() {
    if (passwordField.value.length > 0) {
        togglePassword.style.display = 'inline'; // Show the eye icon
    } else {
        togglePassword.style.display = 'none'; // Hide the eye icon
    }
});

// Toggle password visibility when the eye icon is clicked
togglePassword.addEventListener('click', function() {
    // Toggle the type attribute
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type; // Change type to text or password

    // Change the eye icon to indicate visibility
    if (type === 'password') {
        passwordIcon.src = "/static/icons/hide.png";  // Show "hide" icon
    } else {
        passwordIcon.src = "/static/icons/seen.png";  // Show "seen" icon
    }
});

// Form submission logic
form.addEventListener("submit", function (e) {
    e.preventDefault();  // Prevent form submission
    let formData = new FormData(form);  // Collect form data

    fetch("/user/login_attempt", {
        method: "POST",
        body: formData,
    })
    .then(async (response) => {
        if (response.ok) {
            window.location.href = "/";  // Redirect on successful login
        } else if (response.status === 401 || response.status === 400) {
            let errorResponse = await response.json();  // Parse JSON response
            throw new Error(errorResponse.error);  // Throw error with the extracted message
        } else {
            throw new Error("Server error");  // General server error message
        }
    })
    .catch((error) => {
        console.error("Error:", error);  // Log error to console
        error_paragraph.textContent = error.message;  // Use `error.message` to display the error
        error_paragraph.classList.remove("error--hidden");  // Ensure the error paragraph is visible
    });
});
