
"""
This module defines the User class which handles user authentication and session management.
"""
import uuid
from flask import jsonify, request, session
from pymongo import TEXT
import pandas as pd
from core import database, handlers


class Student:
    """Student class."""
    def search_students(self):
        """Searching students."""
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        student_id = request.form.get('student_id')

        query = {}
        if first_name:
            query["first_name"] = first_name
        if last_name:
            query["last_name"] = last_name
        if email:
            query["email"] = email
        if student_id:
            query["student_id"] = student_id
        if request.form.get('course'):
            query["course"] = request.form.get('course')
        if request.form.get('skills'):
            query["skills"] = request.form.get('skills')

        students = list(database.students_collection.find(query))

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def add_student(self):
        """Adding new student."""
        student = {
            "_id": uuid.uuid1().hex,
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "email": request.form.get('email'),
            "student_id": request.form.get('student_id'),
            "course": request.form.get('course'),
            "skills": request.form.get('skills')
        }
        overwrite = bool(request.form.get('overwrite'))

        if not overwrite and database.students_collection.find_one(
            {"student_id": request.form.get('student_id')}
            ):
            return jsonify({"error": "Student already in database"}), 400

        database.students_collection.insert_one(student)

        if student:
            return jsonify(student), 200

        return jsonify({"error": "Student not added"}), 400


    def get_student_by_id(self, student_id):
        """Getting student."""
        student = database.students_collection.find_one({
            "student_id": student_id
            })

        if student:
            return jsonify(student), 200

        return jsonify({"error": "Student not found"}), 404

    def get_students(self):
        """Getting all students."""
        students = list(database.students_collection.find())

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def update_student(self):
        """Updating student."""
        student = database.students_collection.find_one({
            "student_id": request.form.get('student_id')
            })

        if student:
            database.students_collection.update_one({
                "student_id": request.form.get('student_id')}, {
                    "$set": request.form
                    })
            return jsonify({"message": "Student updated"}), 200

        return jsonify({"error": "Student not found"}), 404

    def delete_student_by_id(self, student_id):
        """Deleting student."""
        student = database.students_collection.find_one({"student_id": student_id})

        if student:
            database.students_collection.delete_one({"student_id": student_id})
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
        student = database.students_collection.find_one({"email": request.form.get('email')})

        if student:
            return jsonify(student), 200

        return jsonify({"error": "Student not found"}), 404

    def get_students_by_course(self):
        """Getting students."""
        students = list(database.students_collection.find({"course": request.form.get('course')}))

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def get_students_by_skills(self):
        """Getting students."""
        students = list(database.students_collection.find({"skills": request.form.get('skills')}))

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def get_students_by_course_and_skills(self):
        """Getting students."""
        students = list(database.students_collection.find({
            "course": request.form.get('course'),
            "skills": request.form.get('skills')
            }))

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def get_students_by_name(self):
        """Getting students by name."""
        # Ensure text index is created on the collection
        database.students_collection.create_index([
            ("first_name", TEXT),
            ("last_name", TEXT)
            ])

        students = list(database.students_collection.find({
            "$text": {
                "$search": f"{request.form.get('first_name')} {request.form.get('last_name')}"
                }
        }))

        if students:
            return jsonify(students), 200

        return jsonify({"error": "No students found"}), 404

    def import_from_csv(self):
        """Importing students from CSV file."""

        if not 'file' in request.files:
            return jsonify({"error": "No file part"}), 400

        if not handlers.allowed_file(request.files['file'].filename, ['csv']):
            return jsonify({"error": "Invalid file type"}), 400

        try:
            file = request.files['file']
            df = pd.read_csv(file)

            students = df.to_dict(orient='records')
            for student in students:
                student["_id"] = uuid.uuid1().hex
                database.students_collection.delete_one({"student_id": student["student_id"]})

            database.students_collection.insert_many(students)
            return jsonify({"message": "Students imported"}), 200
        except (pd.errors.EmptyDataError, pd.errors.ParserError, FileNotFoundError) as e:
            return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    def import_from_xlsx(self):
        """Importing students from Excel file."""

        if not 'file' in request.files:
            return jsonify({"error": "No file part"}), 400

        if not handlers.allowed_file(request.files['file'].filename, ['xlsx', 'xls']):
            return jsonify({"error": "Invalid file type"}), 400

        try:
            file = request.files['file']
            df = pd.read_excel(file)

            students = df.to_dict(orient='records')
            for student in students:
                student["_id"] = uuid.uuid1().hex
                database.students_collection.delete_one({"student_id": student["student_id"]})
            database.students_collection.insert_many(students)

            return jsonify({"message": "Students imported"}), 200
        except (pd.errors.EmptyDataError, pd.errors.ParserError, FileNotFoundError) as e:
            return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    def update_student_by_id(self, student_id, is_student=True):
        """Updating student."""
        student = database.students_collection.find_one({"student_id": student_id})

        if student and not is_student:
            database.students_collection.update_one({"student_id": student_id}, {"$set": request.form})
            return jsonify({"message": "Student updated"}), 200
        
        data = {
            "course": request.form.get('course'),
            "skills": request.form.get('skills')
        }
        if student and is_student:
            database.students_collection.update_one({"student_id": student_id}, {"$set": data})
            return jsonify({"message": "Student updated"}), 200

        return jsonify({"error": "Student not found"}), 404

    def student_login(self):
        """Handle student login."""
        student_id = request.form.get('student_id')
        password = request.form.get('password')

        # Find the student by email
        student = database.students_collection.find_one({"_id": password})

        if student and student.get('student_id') == student_id:
            # Assuming you have a session management system
            del student['_id']
            session['student'] = student
            session['student_logged_in'] = True
            return jsonify({"message": "Login successful"}), 200

        return jsonify({"error": "Invalid email or password"}), 401
    