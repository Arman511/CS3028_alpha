// Select the password fields and eye icons
const passwordField = document.getElementById('passwordField');
const confirmPasswordField = document.getElementById('confirmPasswordField');
const togglePassword = document.getElementById('togglePassword');
const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
const error_paragraph = document.querySelector(".error");
const register_form = document.querySelector(".register_form");

// Initially hide the eye icons
togglePassword.style.display = 'none';
toggleConfirmPassword.style.display = 'none';

// Show/hide the eye icon based on password input
passwordField.addEventListener('input', function() {
    togglePassword.style.display = passwordField.value.length > 0 ? 'inline' : 'none';
});

confirmPasswordField.addEventListener('input', function() {
    toggleConfirmPassword.style.display = confirmPasswordField.value.length > 0 ? 'inline' : 'none';
});

// Toggle password visibility for both fields when the eye icons are clicked
togglePassword.addEventListener('click', function() {
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type; // Change type to text or password

    passwordIcon.src = type === 'password' ? "/static/icons/hide.png" : "/static/icons/seen.png"; // Change icon based on visibility
});

toggleConfirmPassword.addEventListener('click', function() {
    const type = confirmPasswordField.type === 'password' ? 'text' : 'password';
    confirmPasswordField.type = type; // Change type to text or password

    confirmPasswordIcon.src = type === 'password' ? "/static/icons/hide.png" : "/static/icons/seen.png"; // Change icon based on visibility
});


// Form submission logic
register_form.addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent form submission

    // Check if passwords match
    if (passwordField.value !== confirmPasswordField.value) {
        error_paragraph.textContent = "Passwords don't match, Try again.";
        error_paragraph.classList.remove("error--hidden");
        return; // Stop submission if passwords do not match
    }

    // Clear previous error message
    error_paragraph.classList.add("error--hidden");

    let formData = new FormData(register_form);

    fetch("/user/register_attempt", {
        method: "POST",
        body: formData,
    })
    .then(async (response) => {
        if (response.ok) {
            window.location.href = "/";  // Redirect on successful registration
        } else if (response.status === 400) {
            let errorMessage = await response.text();  // Get error text from response
            throw new Error(errorMessage);  // Throw error with message
        } else {
            throw new Error("Server error");  // General server error message
        }
    })
    .catch((error) => {
        console.error("Error:", error);  // Log error to console
        error_paragraph.classList.remove("error--hidden");  // Show error paragraph
        error_paragraph.textContent = error.message;  // Display the error message only
    });
});
