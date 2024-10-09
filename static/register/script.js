document.addEventListener("DOMContentLoaded", () => {
    // Select the password fields and eye icons
    const passwordField = document.getElementById("passwordField");
    const confirmPasswordField = document.getElementById(
        "confirmPasswordField"
    );

    const error_paragraph = document.querySelector(".error");
    const register_form = document.querySelector(".register_form");

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

        fetch("/user/register", {
            method: "POST",
            body: formData,
        })
            .then(async (response) => {
                if (response.ok) {
                    window.location.href = "/"; // Redirect on successful registration
                } else if (response.status === 400) {
                    let errorMessage = await response.text(); // Get error text from response
                    throw new Error(errorMessage); // Throw error with message
                } else {
                    throw new Error("Server error"); // General server error message
                }
            })
            .catch((error) => {
                console.error("Error:", error); // Log error to console
                error_paragraph.classList.remove("error--hidden"); // Show error paragraph
                error_paragraph.textContent = error.message; // Display the error message only
            });
    });
});
