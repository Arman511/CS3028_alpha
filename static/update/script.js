document.addEventListener("DOMContentLoaded", () => {
    const updateForm = document.getElementById("updateForm");

    updateForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(updateForm);

        try {
            const response = await fetch(
                `/student/update/${formData.get("student_id")}`,
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
                window.location.href = "/students/search_students";
            } else {
                const errorElement = document.querySelector(".error");
                errorElement.textContent = "Error updating student";
                errorElement.classList.remove("error--hidden");
            }
        } catch (error) {
            console.error("Error:", error);
            const errorElement = document.querySelector(".error");
            errorElement.textContent = "Error updating student";
            errorElement.classList.remove("error--hidden");
        }
    });
});
