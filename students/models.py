"""
This module defines the User class which handles user authentication and session management.
"""

import uuid
from flask import jsonify, request, session
from pymongo import TEXT
import pandas as pd
from core import database, handlers
from opportunities.models import Opportunity


class Student:
    """Student class."""

    def search_students(self):
        """Searching students."""
        data = request.get_json()
        # Build the query with AND logic
        query = {}
        if data.get("first_name"):
            query["first_name"] = data["first_name"]
        if data.get("last_name"):
            query["last_name"] = data["last_name"]
        if data.get("email"):
            query["email"] = data["email"]
        if data.get("student_id"):
            query["student_id"] = data["student_id"]
        if data.get("course"):
            query["course"] = data["course"]
        if data.get("skills"):
            # Match students with at least one of the provided skills
            query["skills"] = {"$in": data["skills"]}
        if data.get("modules"):
            # Match students with at least one of the provided modules
            query["modules"] = {"$in": data["modules"]}

        students = list(database.students_collection.find(query))

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def add_student(self):
        """Adding new student."""
        student = {
            "_id": uuid.uuid1().hex,
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "student_id": request.form.get("student_id"),
        }
        overwrite = bool(request.form.get("overwrite"))

        if not overwrite and database.students_collection.find_one(
            {"student_id": request.form.get("student_id")}
        ):
            return jsonify({"error": "Student already in database"}), 400

        database.students_collection.insert_one(student)

        if student:
            return jsonify(student), 200

        return jsonify({"error": "Student not added"}), 400

    def get_student_by_id(self, student_id):
        """Getting student."""
        student = database.students_collection.find_one({"student_id": str(student_id)})

        if student:
            return student

        return None

    def get_student_by_uuid(self, _id):
        """Getting student."""
        student = database.students_collection.find_one({"_id": str(_id)})

        if student:
            return student

        return None

    def get_students(self):
        """Getting all students."""
        students = list(database.students_collection.find())

        if students:
            return students

        return []

    def update_student_by_id(self, student_id, student_data):
        """Update student in the database by student_id."""
        # Attempt to update the student directly with the provided data
        result = database.students_collection.update_one(
            {"student_id": str(student_id)},  # Match the student by ID
            {"$set": student_data},  # Update the fields with the new values
        )

        # Return True if the update was successful (i.e., a document was matched and modified)
        if result.matched_count > 0:
            return jsonify({"message": "Student updated"}), 200
        else:
            return jsonify({"error": "Student not found"}), 404

    def delete_student_by_id(self, student_id):
        """Deleting student."""
        student = database.students_collection.find_one({"student_id": str(student_id)})

        if student:
            database.students_collection.delete_one({"student_id": str(student_id)})
            return jsonify({"message": "Student deleted"}), 200

        return jsonify({"error": "Student not found"}), 404

    def delete_students(self):
        """Deleting all students."""
        students = list(database.students_collection.find())

        if students:
            database.students_collection.delete_many({})
            return jsonify({"message": "All students deleted"}), 200

        return jsonify({"error": "No students found"}), 404

    def get_student_by_email(self):
        """Getting student."""
        student = database.students_collection.find_one(
            {"email": request.form.get("email")}
        )

        if student:
            return jsonify(student), 200

        return jsonify({"error": "Student not found"}), 404

    def get_students_by_course(self):
        """Getting students."""
        students = list(
            database.students_collection.find({"course": request.form.get("course")})
        )

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def get_students_by_skills(self):
        """Getting students."""
        students = list(
            database.students_collection.find({"skills": request.form.get("skills")})
        )

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def get_students_by_course_and_skills(self):
        """Getting students."""
        students = list(
            database.students_collection.find(
                {
                    "course": request.form.get("course"),
                    "skills": request.form.get("skills"),
                }
            )
        )

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def get_students_by_name(self):
        """Getting students by name."""
        # Ensure text index is created on the collection
        database.students_collection.create_index(
            [("first_name", TEXT), ("last_name", TEXT)]
        )

        students = list(
            database.students_collection.find(
                {
                    "$text": {
                        "$search": (
                            f"{request.form.get('first_name')} "
                            f"{request.form.get('last_name')}"
                        )
                    }
                }
            )
        )

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def import_from_csv(self):
        """Importing students from CSV file."""

        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        if not handlers.allowed_file(request.files["file"].filename, ["csv"]):
            return jsonify({"error": "Invalid file type"}), 400

        try:
            file = request.files["file"]
            df = pd.read_csv(file)

            students = df.to_dict(orient="records")
            for student in students:
                student["_id"] = uuid.uuid4().hex
                database.students_collection.delete_one(
                    {"student_id": student["student_id"]}
                )
                database.students_collection.insert_one(student)
            return jsonify({"message": "Students imported"}), 200
        except (
            pd.errors.EmptyDataError,
            pd.errors.ParserError,
            FileNotFoundError,
        ) as e:
            return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    def import_from_xlsx(self):
        """Importing students from Excel file."""

        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        if not handlers.allowed_file(request.files["file"].filename, ["xlsx", "xls"]):
            return jsonify({"error": "Invalid file type"}), 400
        try:
            file = request.files["file"]
            df = pd.read_excel(file)

            students = df.to_dict(orient="records")
            for student in students:
                temp_student = {}
                temp_student["_id"] = uuid.uuid4().hex
                temp_student["first_name"] = student["First Name"]
                temp_student["last_name"] = student["Last Name"]
                temp_student["email"] = student["Email (Uni)"]
                if temp_student["email"].split("@")[1] != "abdn.ac.uk":
                    return (
                        jsonify(
                            {
                                "message": (
                                    f"Incorrect student {temp_student['first_name']} "
                                    f"{temp_student['last_name']}"
                                )
                            }
                        ),
                        400,
                    )
                temp_student["student_id"] = str(student["Student Number"])
                if len(str(temp_student["student_id"])) != 8:
                    return (
                        jsonify(
                            {
                                "error": (
                                    f"Invalid student {temp_student['first_name']}, "
                                    f"{temp_student['last_name']}"
                                )
                            }
                        ),
                        400,
                    )
                database.students_collection.delete_one(
                    {"student_id": temp_student["student_id"]}
                )
                database.students_collection.insert_one(temp_student)

            return jsonify({"message": f"{len(students)} students imported"}), 200
        except (
            pd.errors.EmptyDataError,
            pd.errors.ParserError,
            FileNotFoundError,
        ) as e:
            return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    # def update_student_by_id(self, student_id, is_student=True):
    #     """Updating student."""
    #     student = database.students_collection.find_one({"student_id": str(student_id)})

    #     if student and not is_student:
    #         database.students_collection.update_one(
    #             {"student_id": student_id}, {"$set": request.form}
    #         )
    #         return jsonify({"message": "Student updated"}), 200

    #     if "student" not in session:
    #         return jsonify({"error": "You are not logged in"}), 401
    #     if (
    #         is_student
    #         and str(student["student_id"]) != session["student"]["student_id"]
    #     ):
    #         return (
    #             jsonify({"error": "You are not authorized to update this student"}),
    #             403,
    #         )
    #     student["comments"] = request.form.get("comments")
    #     student["skills"] = request.form.get("skills")
    #     student["attempted_skills"] = request.form.get("attempted_skills")
    #     student["has_car"] = request.form.get("has_car")
    #     student["placement_duration"] = request.form.get("placement_duration")
    #     student["modules"] = request.form.get("modules")
    #     student["course"] = request.form.get("course")

    #     if student and is_student:
    #         database.students_collection.update_one(
    #             {"student_id": str(student_id)}, {"$set": student}
    #         )
    #         return jsonify({"message": "Student updated"}), 200

    #     if not is_student:
    #         database.students_collection.delete_one({"student_id": student_id})
    #         database.students_collection.insert_one(request.form)
    #         return jsonify({"message": "Student updated"}), 200

    #     return jsonify({"error": "Student not found"}), 404

    def student_login(self):
        """Handle student login."""
        student_id = request.form.get("student_id")
        password = request.form.get("password")

        # Find the student by email
        student = database.students_collection.find_one({"_id": password})

        if student and str(student.get("student_id")) == student_id:
            # Assuming you have a session management system
            del student["_id"]
            session["student"] = student
            session["student_logged_in"] = True
            return jsonify({"message": "Login successful"}), 200

        return jsonify({"error": "Invalid email or password"}), 401

    def rank_preferences(self, student_id):
        """Sets a students preferences."""
        student = database.students_collection.find_one({"student_id": str(student_id)})

        if not student:
            return jsonify({"error": "Student not found"}), 404

        preferences = [a[5:] for a in request.form.get("ranks").split(",")]
        database.students_collection.update_one(
            {"student_id": str(student_id)}, {"$set": {"preferences": preferences}}
        )
        return jsonify({"message": "Preferences updated"}), 200

    def get_opportunities_by_student(self, student_id):
        """Get opportunities that a student could do"""
        find_student = self.get_student_by_id(student_id)

        if not find_student:
            return jsonify({"error": "Student not found"}), 404

        opportunities = Opportunity().get_opportunities()

        student = find_student
        student["modules"] = set(
            d.strip().replace('"', "")
            for d in student["modules"][1:-1].split(",")
            if d.strip().replace('"', "") != ""
        )

        valid_opportunities = []
        for opportunity in opportunities:
            modules_required = set(
                module.strip().replace('"', "")
                for module in opportunity["modules_required"][1:-1].split(",")
                if module.strip().replace('"', "") != ""
            )

            if modules_required.issubset(student["modules"]):
                if (
                    student["course"] in opportunity["courses_required"]
                    or opportunity["courses_required"] == ""
                ):
                    if opportunity["duration"] in student["placement_duration"]:
                        valid_opportunities.append(opportunity)

        return valid_opportunities
