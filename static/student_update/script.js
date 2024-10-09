document.addEventListener("DOMContentLoaded", () => {
    const updateForm = document.getElementById("updateForm");
    const errorElement = document.querySelector(".error");
    const successElement = document.querySelector(".success");
    updateForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(updateForm);

        try {
            const response = await fetch(
                `/student/details/${formData.get("student_id")}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: formData,
                }
            );

            if (response.ok) {
                const student = await response.json();
                console.log("Student updated:", student);
                successElement.textContent = "Student updated successfully";
                successElement.classList.remove("success--hidden");
                errorElement.classList.add("error--hidden");
            } else {
                errorElement.textContent = "Error updating student";
                errorElement.classList.remove("error--hidden");
                successElement.classList.add("success--hidden");
            }
        } catch (error) {
            console.error("Error:", error);
            const errorElement = document.querySelector(".error");
            errorElement.textContent = "Error updating student";
            errorElement.classList.remove("error--hidden");
            successElement.classList.add("success--hidden");
        }
    });
});
