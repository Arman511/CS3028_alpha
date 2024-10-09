"""
    Registers student-related routes to the given Flask application.
    Routes:
        - POST /students/add_student: Adds a new student. Requires login.
        - POST /students/upload_csv: Uploads students from a CSV file. Requires login.
        - POST /students/upload_xlsx: Uploads students from an XLSX file. Requires login.
        - GET /students/search: Renders the student search page. Requires login.
        - POST /students/search_students: Searches for students. Requires login.
        - DELETE /students/delete_student/<int:student_id>: Deletes a student by ID. Requires login.
        - GET, POST /student/update/<int:student_id>: Updates a student by ID. Requires login.
    Args:
        app (Flask): The Flask application instance to which the routes will be added.
"""
from flask import redirect, render_template, request, session
from core import handlers
from courses.models import Course
from skills.models import Skill
from .models import Student

def add_student_routes(app):
    """Add student routes."""
    @app.route('/students/add_student', methods=['POST'])
    @handlers.login_required
    def register_student_attempt():
        """Adding new student."""
        return Student().add_student()

    @app.route('/students/upload_csv', methods=['POST'])
    @handlers.login_required
    def upload_csv():
        """Route to upload students from a CSV file."""
        return Student().import_from_csv()


    @app.route('/students/upload_xlsx', methods=['POST'])
    @handlers.login_required
    def upload_xlsx():
        """Route to upload students from a XLSX file."""
        return Student().import_from_xlsx()

    @app.route('/students/search')
    @handlers.login_required
    def search_page():
        """Getting student."""
        return render_template("search_student.html",
                               skills=Skill().get_skills(),
                               courses=Course().get_courses())

    @app.route('/students/search_students', methods=['POST'])
    @handlers.login_required
    def search_students():
        """Getting student."""
        return Student().search_students()

    @app.route('/students/delete_student/<int:student_id>', methods=['DELETE'])
    @handlers.login_required
    def delete_student(student_id):
        """Delete student."""
        return Student().delete_student_by_id(student_id)

    @app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
    @handlers.login_required
    def update_student(student_id):
        """Update student."""
        if request.method == 'POST':
            return Student().update_student_by_id(student_id, False)
        student = Student().get_student_by_id(student_id)

        return render_template("update_student.html",
                               student=student,skills=Skill().get_skills(),
                               courses=Course().get_courses())

    @app.route('/student/login', methods=['GET', 'POST'])
    def login_student():
        """Logins a student"""
        if request.method == 'POST':
            return Student().student_login()
        return render_template("student_login.html")

    @app.route('/student/signout')
    @handlers.student_login_required
    def signout_student():
        session.clear()
        return redirect('/student/login')

    @app.route('/student/details<int:student_id>', methods=['GET', 'POST'])
    @handlers.student_login_required
    def student_details(student_id):
        """Getting student."""
        if session['student_id'] != student_id:
            session.clear()
            return redirect('/student/login')
        if request.method == 'POST':
            return Student().update_student_by_id(student_id,  True)
        student = Student().get_student_by_id(student_id)
        return render_template("student_details.html", student=student,
                               skills=Skill().get_skills(), courses=Course().get_courses())
