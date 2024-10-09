document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("searchForm");
    const studentTable = document.getElementById("student-table");

    searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(searchForm);

        try {
            const response = await fetch("/students/search_students", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: formData,
            });

            if (response.ok) {
                const students = await response.json();
                console.log("Students found:", students);
                // Handle displaying students
                const errorElement = document.querySelector(".error");
                errorElement.classList.add("error--hidden");
                errorElement.textContent = "";

                // Code to display students in the table
                studentTable.innerHTML = ""; // Clear any existing rows

                students.forEach((student) => {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${student.first_name}</td>
                        <td>${student.last_name}</td>
                        <td>${student.email}</td>
                        <td>${student.student_id}</td>
                        <td>${student.course}</td>
                        <td>${student.skills}</td>
                        <td>
                            <button class="update-button">Update</button>
                            <button class="delete-button">Delete</button>
                        </td>
                    `;

                    // Add event listeners for the buttons
                    const updateButton = row.querySelector(".update-button");
                    const deleteButton = row.querySelector(".delete-button");

                    updateButton.addEventListener("click", () => {
                        // Code to handle update action
                        console.log(
                            `Update student with ID: ${student.student_id}`
                        );
                        window.location.href = `/student/update/${student.student_id}`;
                        // Implement update logic here
                    });

                    deleteButton.addEventListener("click", async () => {
                        // Code to handle delete action
                        console.log(
                            `Delete student with ID: ${student.student_id}`
                        );
                        try {
                            const response = await fetch(
                                `/students/delete_student/${student.student_id}`,
                                {
                                    method: "DELETE",
                                }
                            );

                            if (response.ok) {
                                // Remove the row from the table
                                row.remove();
                                console.log(
                                    `Student with ID: ${student.student_id} deleted successfully`
                                );
                            } else {
                                const error = await response.json();
                                console.error("Error:", error);
                                // Handle displaying error message
                                const errorElement =
                                    document.querySelector(".error");
                                errorElement.classList.remove("error--hidden");
                                errorElement.textContent = error.message;
                            }
                        } catch (error) {
                            console.error("Fetch error:", error);
                            // Handle displaying fetch error
                        }
                    });

                    studentTable.appendChild(row);
                });
            } else {
                const error = await response.json();
                console.error("Error:", error);
                // Handle displaying error message
                const errorElement = document.querySelector(".error");
                errorElement.classList.remove("error--hidden");
                errorElement.textContent = error.message;
            }
        } catch (error) {
            console.error("Fetch error:", error);
            // Handle displaying fetch error
        }
    });
});
