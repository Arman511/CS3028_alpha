"""
Handles routes for the user module.
"""

from datetime import datetime
from flask import redirect, render_template, session, request
from algorithm.matching import Matching
from core import database, handlers
from employers.models import Employers
from students.models import Student
from .models import User


def add_user_routes(app, cache):
    """Add user routes."""

    @app.route("/user/register", methods=["GET", "POST"])
    def register():
        """Give page to register a new user."""
        if request.method == "POST":
            return User().register()
        return render_template("user/register.html")

    @app.route("/user/login", methods=["GET", "POST"])
    def login():
        """Gives login form to user."""
        if request.method == "POST":
            return User().login()
        if "logged_in" in session:
            return redirect("/")
        return render_template("user/login.html")

    @app.route("/user/change_password", methods=["GET", "POST"])
    def change_password():
        """Change user password."""
        if request.method == "POST":
            return User().change_password()
        return render_template("user/change_password.html")

    @app.route("/user/deadline", methods=["GET", "POST"])
    @handlers.login_required
    def deadline():
        """Change deadline."""
        if request.method == "POST":
            return User().change_deadline()

        return render_template(
            "user/deadline.html",
            details_deadline=database.get_details_deadline(),
            student_ranking_deadline=database.get_student_ranking_deadline(),
            opportunities_ranking_deadline=database.get_opportunities_ranking_deadline(),
        )

    @app.route("/user/problem", methods=["GET"])
    @handlers.login_required
    def problems():
        problems = []

        students = Student().get_students()
        passed_details_deadline = database.is_past_details_deadline()
        passed_student_ranking_deadline = database.is_past_student_ranking_deadline()
        passed_opportunities_ranking_deadline = (
            database.is_past_opportunities_ranking_deadline()
        )

        for student in students:
            if "modules" not in student:
                problems.append(
                    {
                        "description": f"Student {student['student_id']}, has not filled in their details "
                        + (
                            "the deadline has passed so can not complete it"
                            if passed_details_deadline
                            else " the deadline has not passed yet"
                        ),
                        "email": student["email"],
                    }
                )

            if "preferences" not in student:
                problems.append(
                    {
                        "description": f"Student {student['student_id']}, has not ranked their opportunities "
                        + (
                            "the deadline has passed so can not complete it"
                            if passed_student_ranking_deadline
                            else " the deadline has not passed yet"
                        ),
                        "email": student["email"],
                    }
                )

        opportunities = database.opportunities_collection.find()

        for opportunity in opportunities:
            if "preferences" not in opportunity:
                problems.append(
                    {
                        "description": f"Opportunity {opportunity['title']} with id {opportunity['_id']}, has not ranked their students "
                        + (
                            "the deadline has passed so can not complete it"
                            if passed_opportunities_ranking_deadline
                            else " the deadline has not passed yet"
                        ),
                        "email": Employers().get_employer_by_id(
                            opportunity["employer_id"]
                        )["email"],
                    }
                )

        return render_template("user/problems.html", problems=problems)

    @app.route("/user/send_match_email", methods=["POST"])
    @handlers.login_required
    def send_match_email():
        """Send match email."""
        return User().send_match_email()

    @app.route("/user/matching", methods=["GET"])
    @handlers.login_required
    @cache.cached(timeout=300)
    def matching():
        if not database.is_past_opportunities_ranking_deadline():
            return render_template(
                "user/past_deadline.html",
                referrer=request.referrer,
                data=f"The final deadline must have passed to do matching, wait till {database.get_opportunities_ranking_deadline()}",
            )

        students = list(database.students_collection.find())
        valid_students = []
        unmatched_students = []
        for student in students:
            if "preferences" in student:
                valid_students.append(student)
                continue
            temp = {}
            temp["_id"] = student["_id"]
            temp["student_id"] = student["student_id"]
            temp["email"] = student["email"]
            temp["name"] = f"{student['first_name']} {student['last_name']}"
            temp["reason"] = "Student has not ranked their opportunities"
            unmatched_students.append(temp)

            # """Put this for an eirlier time, maybe at system start"""
            # opp_for_student = Student().get_opportunities_by_student(student["student_id"])
            # random.shuffle(opp_for_student)
            # student["preferences"] =  opp_for_student
            # valid_students.append(student)

        opportunities = list(database.opportunities_collection.find())
        valid_opportunities = []
        for opportunity in opportunities:
            if "preferences" in opportunity:
                valid_opportunities.append(opportunity)
                continue

        students_preference = {}

        for student in valid_students:
            students_preference[student["_id"]] = student["preferences"]

        opportunities_preference = {}
        for opportunity in valid_opportunities:
            temp = {}
            temp["positions"] = opportunity["spots_available"]
            for i, student in enumerate(opportunity["preferences"]):
                temp[student] = i + 1
            opportunities_preference[opportunity["_id"]] = temp
        match = Matching(students_preference, opportunities_preference)
        result = match.find_best_match()
        matches_list = [
            {"opportunity": opportunity, "students": students}
            for opportunity, students in result[1].items()
        ]
        for student_id in result[0]:
            student = next((s for s in students if s["_id"] == student_id), None)
            if student is None:
                continue
            temp = {}
            temp["_id"] = student_id
            temp["student_id"] = student["student_id"]
            temp["email"] = student["email"]
            temp["name"] = f"{student['first_name']} {student['last_name']}"
            temp["reason"] = "Student was not matched"
            unmatched_students.append(temp)

        students_map = {student["_id"]: student for student in students}
        opportunities_map = {
            opportunity["_id"]: opportunity for opportunity in opportunities
        }
        employers = list(database.employers_collection.find())
        employers_map = {employer["_id"]: employer for employer in employers}
        return render_template(
            "user/matching.html",
            not_matched=unmatched_students,
            matches=matches_list,
            students_map=students_map,
            employers_map=employers_map,
            opportunities_map=opportunities_map,
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
