document.addEventListener("DOMContentLoaded", () => {
    let form = document.querySelector(".login_form");
    let error_paragraph = document.querySelector(".error");
    let submitButton = form.querySelector("input[type='submit']");
    let otpModal = document.getElementById("otpModal");
    let otpInput = document.getElementById("otpInput");
    let otpErrorParagraph = document.querySelector(".otp_error");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        submitButton.disabled = true;

        let formData = new FormData(form);

        try {
            const response = await fetch("/employers/login", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                // Show OTP modal
                otpModal.style.display = "flex";
            } else {
                error_paragraph.textContent = "Email was invalid";
                error_paragraph.classList.remove("error--hidden");
            }
        } catch (error) {
            console.log(error);
            error_paragraph.textContent = "Invalid";
            error_paragraph.classList.remove("error--hidden");
        } finally {
            submitButton.disabled = false;
            otpInput.value = "";
        }
    });

    window.submitOtp = async function () {
        let otp = otpInput.value;
        if (otp) {
            let otpFormData = new FormData();
            otpFormData.append("otp", otp);

            try {
                const otp_response = await fetch("/employers/otp", {
                    method: "POST",
                    body: otpFormData,
                });

                if (otp_response.ok) {
                    window.location.href = "/employers/home";
                } else {
                    error_paragraph.textContent = "OTP was invalid";
                    error_paragraph.classList.remove("error--hidden");
                    otpErrorParagraph.textContent = "OTP was invalid";
                    otpErrorParagraph.classList.remove("error--hidden");
                }
            } catch (error) {
                console.log(error);
                otpErrorParagraph.textContent = "An error occurred";
                otpErrorParagraph.classList.remove("error--hidden");
            } finally {
                hideOtpModal();
            }
        } else {
            otpErrorParagraph.textContent = "OTP was empty";
            otpErrorParagraph.classList.remove("error--hidden");
        }
    };

    window.cancelOtp = function () {
        error_paragraph.textContent = "OTP entry canceled.";
        error_paragraph.classList.remove("error--hidden");
        hideOtpModal();
    };

    function hideOtpModal() {
        otpModal.style.display = "none";
    }
});
